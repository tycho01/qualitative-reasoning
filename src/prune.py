# Importing the Libraries
import copy
from typing import List, Dict, Tuple, Set
from qr_types import *

def check_influence(source_state: EntityState, target_state: EntityState) -> bool:
    '''check whether all the influences hold for the destination state'''

    # Obtaining the state and the relations for the system
    state1 = source_state.state
    state2 = target_state.state
    derivatives1 = state_derivatives(state1)
    derivatives2 = state_derivatives(state2)
    relations = source_state.entity.relations

    # Dictionary to keep track of the derivative directions of dependant quantities
    target_quantities = relation_effects(state1, relations)
    # Determine the overall derivative direction for the target quantities
    relation_derivatives = {k: combine_derivatives(directions) for k, directions in target_quantities.items()}
    # check if state2 derivatives are compatible with relation_derivatives
    # i.e. ensure each relation_derivative equals state2's or is a QUESTION: filter out QUESTIONs then check other vals match. 
    known = [k for k, v in relation_derivatives.items() if v != DerivativeDirection.QUESTION]
    derivatives_match = {k: derivatives2[k]         for k in known} == \
                        {k: relation_derivatives[k] for k in known}
    if not derivatives_match:
        return False

    # - check magnitude changes from state1 to state2 match the state2 derivatives
    change_derivatives = check_magnitude_changes(state1, state2)
    magnitudes_match = change_derivatives == derivatives1
    # TODO:
    #   - any point magnitudes *must* change a step according to the derivative (diff == derivative)
    #   - any range magnitudes *might* change a step according to the derivative.
    #     generate any combinations of changing range magnitudes by itertools.product to generate potential next states!
    # TODO: ensure derivatives are zero when the magnitudes are at an extreme
    return magnitudes_match

def state_derivatives(state: Dict[str, QuantityPair]) -> Dict[str, DerivativeDirection]:
    '''return the derivatives of a state'''
    return {k: qty.derivative for k, qty in state.items()}

def relation_effects(state: Dict[str, QuantityPair], relations: List[Relation]) -> Dict[str, Set[DerivativeDirection]]:
    '''for each quantity in a state find the effects of the relationships working on that quantity'''
    # TODO: figure out if the present derivatives should be included in these target_quantities.
    # if absent, we still need to reconcile these as well. if present, we might confuse
    # positive derivatives influenced down with vice versa, which are different as the former
    # cannot end up as direction negative due to the continuity rule (0 is in-between). 
    target_quantities = {k: set() for k in state}
    for relation in relations:
        if type(relation) != ValueCorrespondence:  # skip ValueCorrespondence which are different
            target_k = relation.b.name
            qty1 = state[relation.a.name]
            correl = relation.correlation
            # add the derivative direction
            target_quantities[target_k].add(
                perform_indirect_influence(correl, qty1.derivative)
                if type(relation) == Proportional else
                perform_direct_influence(correl, qty1.magnitude.value))
    return target_quantities

def combine_derivatives(directions_: Set[DerivativeDirection]) -> DerivativeDirection:
    '''obtain a DerivativeDirection by combining a set of them. this may give DerivativeDirection.QUESTION.'''
    directions = directions_ - {DerivativeDirection.NEUTRAL}
    size = len(set(directions))
    return DerivativeDirection.NEUTRAL if size == 0 else list(directions)[0] if size == 1 else DerivativeDirection.QUESTION

def check_value_correspondence(entity_state: EntityState) -> bool:
    '''check if a state is deemed valid by its value correspondence rules'''
    state = entity_state.state
    entity = entity_state.entity
    for relation in entity.relations:
        if type(relation) == ValueCorrespondence:
            if not qty_matches(state, relation.a) == qty_matches(state, relation.b):
                return False
    return True

def perform_direct_influence(direct_influence_type: RelationDirection, source_quantity_magnitude: int) -> DerivativeDirection:
    type_sign = -1 if direct_influence_type == RelationDirection.NEGATIVE else 1
    source_quantity_magnitude_sign = 1 if source_quantity_magnitude > 0 else 0 if source_quantity_magnitude == 0 else -1
    resulting_sign = type_sign * source_quantity_magnitude_sign
    return DerivativeDirection.POSITIVE if resulting_sign == 1 else DerivativeDirection.NEUTRAL if resulting_sign == 0 else DerivativeDirection.NEGATIVE

def perform_indirect_influence(indirect_influence_type: RelationDirection, source_quantity_direction: Enum) -> DerivativeDirection:
    type_sign = -1 if indirect_influence_type == RelationDirection.NEGATIVE else 1
    source_quantity_direction_sign = 1 if source_quantity_direction == DerivativeDirection.POSITIVE else 0 if source_quantity_direction == DerivativeDirection.NEUTRAL else -1 if source_quantity_direction == DerivativeDirection.NEGATIVE else 2
    resulting_sign = type_sign * source_quantity_direction_sign
    return DerivativeDirection.POSITIVE if resulting_sign == 1 else DerivativeDirection.NEUTRAL if resulting_sign == 0 else DerivativeDirection.NEGATIVE if resulting_sign == -1 else DerivativeDirection.QUESTION
 
def qty_matches(state: Dict[str, QuantityPair], qty_pair: Tuple[str, Enum]) -> bool:
    '''check if a state quantity matches a given value. function for internal use in check_value_correspondence.'''
    (qty_name, val) = qty_pair
    return val == state[qty_name].magnitude

def check_magnitude_changes(state1: Dict[str, QuantityPair], state2: Dict[str, QuantityPair]) -> Dict[str, DerivativeDirection]:
    '''calculate magnitude changes from state1 to state2'''
    return {
        k: num_to_direction(
            state2[k].magnitude.value -
            state1[k].magnitude.value
        ) for k in state1
    }

def num_to_direction(num: int) -> DerivativeDirection:
    '''get a DerivativeDirection from a number's sign'''
    return DerivativeDirection.NEUTRAL if num == 0 else \
           DerivativeDirection.POSITIVE if num > 0 else \
           DerivativeDirection.NEGATIVE

def check_continuous(stateA: EntityState, stateB: EntityState) -> bool:
    '''check that two states' magnitudes/derivatives aren't too far apart'''
    quantities = stateA.entity.quantities
    qty_keys = quantities.keys()
    for k in qty_keys:
        a_pair = stateA.state[k]
        b_pair = stateB.state[k]
        # derivatives are OK iff the same or either is neutral, leaving positive/negative the only bad combo
        if {a_pair.derivative, b_pair.derivative} == {DerivativeDirection.NEGATIVE, DerivativeDirection.POSITIVE}:
            return False
        # magnitudes are OK if equal or subsequent (in either direction)
        index = {v:k for k,v in enumerate(quantities[k].quantitySpace.__members__.values())}
        if abs(index[a_pair.magnitude] - index[b_pair.magnitude]) > 1:
            return False
    return True

def check_point_range(stateA: EntityState, stateB: EntityState) -> bool:
    '''confirm that range magnitudes changed only if no point magnitudes changed'''
    point_changed = False
    range_changed = False
    quantities = stateA.entity.quantities
    qty_keys = quantities.keys()
    for k in qty_keys:
        a_val = stateA.state[k].magnitude
        b_val = stateB.state[k].magnitude
        changed = a_val != b_val
        if changed:
            was_point = a_val.value % 2 == 0  # point values are encoded as even numbers
            if was_point:
                point_changed = True
            else:
                range_changed = True
    return not (point_changed and range_changed)

def filter_states(entity_states: List[EntityState]) -> List[EntityState]:
    '''filter a list of entity states to those states deemed valid by valid correspondence'''
    return list(filter(check_value_correspondence, entity_states))

def check_not_equal(stateA: EntityState, stateB: EntityState) -> bool:
    '''confirm two states are distinct'''
    return stateA != stateB

def can_transition(a: EntityState, b: EntityState) -> bool:
    '''confirm a source state can transition into a target state'''
    return check_influence(a, b) and check_continuous(a, b) and check_point_range(a, b) and check_not_equal(a, b)
