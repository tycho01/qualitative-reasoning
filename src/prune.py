# Importing the Libraries
import copy
from typing import List, Dict, Tuple
from qr_types import *

def check_influence(source_state: EntityState, target_state: EntityState) -> bool:
    '''check whether all the influences hold'''

    # Obtaining the state and the relations for the system
    state1 = source_state.state
    state2 = target_state.state
    relations = source_state.entity.relations

    # Test state for verification
    test_state = copy.deepcopy(state1)

    # Dictionary to keep track of the derivative directions of dependant quantities
    target_quantities = {}
    for relation in relations:
        if type(relation) != ValueCorrespondence:  # skip ValueCorrespondence which are different
            # Retrieving the names of the source and target quantities
            source_quantity_name = relation.a.name
            target_quantity_name = relation.b.name
            source_quantity_magnitude = state1[source_quantity_name].magnitude.value
            source_quantity_direction = state1[source_quantity_name].derivative

            # Create a list for the target quantity if not present in the dictionary
            if target_quantity_name not in target_quantities:
                target_quantities[target_quantity_name] = []
            
           # If it is a direct influence
            if type(relation) == Influence:
                target_quantities[target_quantity_name].append(perform_direct_influence(relation.correlation.value, source_quantity_magnitude))
            # If it is a proportional influence
            elif type(relation) == Proportional:
                target_quantities[target_quantity_name].append(perform_indirect_influence(relation.correlation.value, source_quantity_direction))
            
    # Determining the overall derivative direction for the target quantities
    for target_quantity in target_quantities:
        directions = target_quantities[target_quantity]
        target_quantity_magnitude = test_state[target_quantity].magnitude
        target_quantity_direction = test_state[target_quantity].derivative
        if len(set(directions)) == 1:
            if directions[0] == DerivativeDirection.POSITIVE:
                target_quantity_direction = DerivativeDirection.POSITIVE
            elif directions[0] == DerivativeDirection.NEGATIVE:
                target_quantity_direction = DerivativeDirection.NEGATIVE
            elif directions[0] == DerivativeDirection.QUESTION:
                target_quantity_direction = DerivativeDirection.QUESTION
            elif directions[0] == DerivativeDirection.NEUTRAL:
                pass
        elif len(set(directions)) == 2:
            if DerivativeDirection.NEUTRAL in set(directions):
                if DerivativeDirection.POSITIVE in set(directions):
                    target_quantity_direction = DerivativeDirection.POSITIVE
                elif DerivativeDirection.NEGATIVE in set(directions):
                    target_quantity_direction = DerivativeDirection.NEGATIVE
                elif DerivativeDirection.QUESTION in set(directions):
                    target_quantity_direction = DerivativeDirection.QUESTION
            else:
                target_quantity_direction = DerivativeDirection.QUESTION
        elif len(set(directions)) > 2:
            target_quantity_direction = DerivativeDirection.QUESTION

        test_state[target_quantity] = (target_quantity_magnitude, target_quantity_direction)
    
    # Returning if the destination state is valid or not
    return test_state == state2

def check_value_correspondence(entity_state: EntityState) -> bool:
    '''check if a state is deemed valid by its value correspondence rules'''
    state = entity_state.state
    entity = entity_state.entity
    for relation in entity.relations:
        if type(relation) == ValueCorrespondence:
            if not qty_matches(state, relation.a) == qty_matches(state, relation.b):
                return False
    return True

def perform_direct_influence(direct_influence_type: int, source_quantity_magnitude: int) -> int:
    type_sign = -1 if direct_influence_type == RelationDirection.NEGATIVE.value else 1
    source_quantity_magnitude_sign = 1 if source_quantity_magnitude > 0 else 0 if source_quantity_magnitude == 0 else -1
    resulting_sign = type_sign * source_quantity_magnitude_sign
    return DerivativeDirection.POSITIVE.value if resulting_sign == 1 else DerivativeDirection.NEUTRAL.value if resulting_sign == 0 else DerivativeDirection.NEGATIVE.value

def perform_indirect_influence(indirect_influence_type: int, source_quantity_direction: Enum) -> int:
    type_sign = -1 if indirect_influence_type == RelationDirection.NEGATIVE.value else 1
    source_quantity_direction_sign = 1 if source_quantity_direction == DerivativeDirection.POSITIVE else 0 if source_quantity_direction == DerivativeDirection.NEUTRAL else -1 if source_quantity_direction == DerivativeDirection.NEGATIVE else 2
    resulting_sign = type_sign * source_quantity_direction_sign
    return DerivativeDirection.POSITIVE.value if resulting_sign == 1 else DerivativeDirection.NEUTRAL.value if resulting_sign == 0 else DerivativeDirection.NEGATIVE.value if resulting_sign == -1 else DerivativeDirection.QUESTION.value
 
def qty_matches(state: Dict[str, QuantityPair], qty_pair: Tuple[str, Enum]) -> bool:
    '''check if a state quantity matches a given value. function for internal use in check_value_correspondence.'''
    (qty_name, val) = qty_pair
    return val == state[qty_name].magnitude

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
