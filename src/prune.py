# Importing the Libraries
import copy
from typing import List, Dict, Tuple, Set
from qr_types import *

def check_influence(source_state: EntityState, target_state: EntityState) -> bool:
    '''check whether all the influences hold for the destination state'''
    state1 = source_state.state
    state2 = target_state.state
    return derivatives_match(state1, state2, source_state.entity.relations) and \
            magnitudes_match(state1, state2)

def derivatives_match(state1: Dict[str, QuantityPair], state2: Dict[str, QuantityPair], relations: List[Relation]) -> bool:
    '''check derivative changes given the quantity relationships.'''
    derivatives1 = state_derivatives(state1)
    derivatives2 = state_derivatives(state2)
    # Dictionary to keep track of the derivative directions of dependant quantities
    effect_sets = relation_effects(state1, relations)
    # Determine the overall derivative direction for the target quantities
    relation_derivatives = {k: combine_derivatives(directions) for k, directions in effect_sets.items()}
    # check if state2 derivatives are compatible with relation_derivatives:
    # filter out QUESTIONs
    known = [k for k, v in relation_derivatives.items() if v != Direction.QUESTION]

    # check other vals add up, i.e. as close to the combined effect in state2 
    # as in state1. note that while this may not filter out jumps from negative
    # to positive, these will be caught in the continuous check instead.
    for k in known:
        effect = relation_derivatives[k]
        change = compare_derivatives(derivatives1[k], derivatives2[k])
        if not change in {Direction.NEUTRAL, effect}:
            return False
    return True

def compare_derivatives(old: Direction, new: Direction) -> Direction:
    '''return a relative Direction between Directions. if equal yields Neutral (rather than Question).'''
    return Direction.NEUTRAL if old == new else Direction.POSITIVE if new.value > old.value else Direction.NEGATIVE

def magnitudes_match(state1: Dict[str, QuantityPair], state2: Dict[str, QuantityPair]) -> bool:
    '''check magnitude changes from state1 to state2 match the state2 derivatives'''
    change_derivatives = check_magnitude_changes(state1, state2)
    for k in state1:
        pair1 = state1[k]
        mag1 = pair1.magnitude
        der1 = pair1.derivative
        change = change_derivatives[k]
        if is_point(mag1):
            # point magnitudes *must* change a step according to the derivative (diff == derivative)
            if change != der1:
                return False
        else:
            # range magnitudes *might* change a step according to the derivative.
            if not change in {Direction.NEUTRAL, der1}:
                return False
    return True

# TODO: ensure this change will not get filtered out by other checks!
def check_extremes(entity_state: EntityState) -> bool:
    '''ensure derivatives are clipped when the magnitudes are at an extreme point'''
    state = entity_state.state
    quantities = entity_state.entity.quantities
    for k, pair in state.items():
        mag = pair.magnitude
        der = pair.derivative
        enum = quantities[k].quantitySpace
        side = extreme_direction(mag, enum)
        if is_point(mag) and der == side and der != Direction.NEUTRAL:
            return False
    return True

def extreme_direction(magnitude: Enum, enum: EnumMeta) -> Direction:
    '''get a direction from a magnitude based on whether it is at the
       high extreme (positive), low (negative), or in between (neutral).'''
    val = magnitude.value
    vals = [mag.value for mag in dict(enum.__members__).values()]
    return Direction.NEGATIVE if val == min(vals) else \
           Direction.POSITIVE if val == max(vals) else \
           Direction.NEUTRAL

def state_derivatives(state: Dict[str, QuantityPair]) -> Dict[str, Direction]:
    '''return the derivatives of a state'''
    return {k: qty.derivative for k, qty in state.items()}

def relation_effects(state: Dict[str, QuantityPair], relations: List[Relation]) -> Dict[str, Set[Direction]]:
    '''for each quantity in a state find the effects of the relationships working on that quantity'''
    target_quantities = {k: set() for k in state}
    for relation in relations:
        if type(relation) != ValueCorrespondence:  # skip ValueCorrespondence which are different
            target_k = relation.b.name
            qty1 = state[relation.a.name]
            correl = relation.correlation
            # add the derivative direction
            target_quantities[target_k].add(
                indirect_influence(correl, qty1.derivative)
                if type(relation) == Proportional else
                direct_influence(correl, qty1.magnitude.value))
    return target_quantities

def combine_derivatives(directions_: Set[Direction]) -> Direction:
    '''obtain a Direction by combining a set of them. this may give Direction.QUESTION.'''
    directions = directions_ - {Direction.NEUTRAL}
    size = len(set(directions))
    return Direction.NEUTRAL if size == 0 else list(directions)[0] if size == 1 else Direction.QUESTION

def check_value_correspondence(entity_state: EntityState) -> bool:
    '''check if a state is deemed valid by its value correspondence rules'''
    state = entity_state.state
    entity = entity_state.entity
    for relation in entity.relations:
        if type(relation) == ValueCorrespondence:
            if not qty_matches(state, relation.a) == qty_matches(state, relation.b):
                return False
    return True

def direct_influence(relation: Direction, magnitude: int) -> Direction:
    '''calculate the effect of an influence relationship given a magnitude.
       note that magnitudes are presumed to be encoded such that signs of
       their values match, i.e. positive as positive, vice versa, 0 as 0.
    '''
    return num_to_direction(to_sign(relation) * magnitude)

def indirect_influence(relation: Direction, derivative: Enum) -> Direction:
    '''calculate the effect of a proportional relationship given a derivative.'''
    return num_to_direction(to_sign(relation) * to_sign(derivative))
 
def qty_matches(state: Dict[str, QuantityPair], qty_pair: Tuple[str, Enum]) -> bool:
    '''check if a state quantity matches a given value. function for internal use in check_value_correspondence.'''
    (qty_name, val) = qty_pair
    return val == state[qty_name].magnitude

def check_magnitude_changes(state1: Dict[str, QuantityPair], state2: Dict[str, QuantityPair]) -> Dict[str, Direction]:
    '''calculate magnitude changes from state1 to state2'''
    return {
        k: num_to_direction(
            state2[k].magnitude.value -
            state1[k].magnitude.value
        ) for k in state1
    }

def num_to_direction(num: int) -> Direction:
    '''get a Direction from a number's sign'''
    return Direction.NEUTRAL if num == 0 else \
           Direction.POSITIVE if num > 0 else \
           Direction.NEGATIVE

def to_sign(direction: Direction) -> int:
    '''convert a Direction to a sign (1, 0, -1)'''
    return 1 if direction == Direction.POSITIVE else \
          -1 if direction == Direction.NEGATIVE else 0

def check_continuous(stateA: EntityState, stateB: EntityState) -> bool:
    '''check that two states' magnitudes/derivatives aren't too far apart'''
    quantities = stateA.entity.quantities
    qty_keys = quantities.keys()
    for k in qty_keys:
        a_pair = stateA.state[k]
        b_pair = stateB.state[k]
        # derivatives are OK iff the same or either is neutral, leaving positive/negative the only bad combo
        if {a_pair.derivative, b_pair.derivative} == {Direction.NEGATIVE, Direction.POSITIVE}:
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
        if a_val != b_val:
            if is_point(a_val):
                point_changed = True
            else:
                range_changed = True
    return not (point_changed and range_changed)

def is_point(magnitude: Enum) -> bool:
    '''check if a magnitude is a point value. presumes point values are encoded as even, ranges as odd numbers.'''
    return magnitude.value % 2 == 0

def filter_states(entity_states: List[EntityState]) -> List[EntityState]:
    '''filter a list of entity states to those states deemed valid by valid correspondence'''
    return list(filter(state_valid, entity_states))

def check_not_equal(stateA: EntityState, stateB: EntityState) -> bool:
    '''confirm two states are distinct'''
    return stateA != stateB

def state_valid(entity_state: EntityState) -> bool:
    '''confirm a state is valid based on value correspondence and extremity checks'''
    return check_value_correspondence(entity_state) and check_extremes(entity_state)

def can_transition(a: EntityState, b: EntityState) -> bool:
    '''confirm a source state can transition into a target state'''
    return check_influence(a, b) and check_continuous(a, b) and check_point_range(a, b) and check_not_equal(a, b)
