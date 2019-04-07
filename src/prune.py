# Importing the Libraries
import copy
from typing import List, Dict, Tuple, Set
import itertools
from qr_types import *

def next_states(entity_state: EntityState) -> List[EntityState]:
    a = entity_state
    return list(filter(lambda b: check_transition(a, b), [EntityState(entity_state.entity, zip_pair(pair)) for pair in itertools.product(
        next_magnitudes(entity_state),
        next_derivatives(entity_state),
    )]))

def zip_pair(tpl: Tuple[Dict[str, Enum], Dict[str, Direction]]) -> Dict[str, QuantityPair]:
    (magnitude_dict, derivative_dict) = tpl
    return {k: QuantityPair(magnitude, derivative_dict[k]) for k, magnitude in magnitude_dict.items()}

# TODO: incorporate transformation based on check_extremes
def next_derivatives(entity_state: EntityState) -> List[Dict[str, Direction]]:
    entity = entity_state.entity
    relations = entity.relations
    state = entity_state.state
    derivatives = state_derivatives(state)
    # Dictionary to keep track of the derivative directions of dependant quantities
    effect_sets = relation_effects(state, relations)
    # Determine the overall derivative direction for the target quantities
    relation_derivatives = {k: combine_derivatives(directions) for k, directions in effect_sets.items()}
    # check if state2 derivatives are compatible with relation_derivatives:
    # k, derivative = list(derivatives.items())[0]
    next_derivatives = {k:
            list(map(lambda x: (k, x), {derivative, move_derivative(derivative, relation_derivatives[k])}))
        for k, derivative in derivatives.items()}
    derivative_combinations = list(map(dict, itertools.product(*next_derivatives.values())))
    return derivative_combinations

def move_derivative(derivative: Direction, effect: Direction) -> Direction:
    return {Direction.NEUTRAL} if {derivative, effect} == {Direction.POSITIVE, Direction.NEGATIVE} else \
        set([derivative]).union(move_derivative(derivative, Direction.POSITIVE)).union(move_derivative(derivative, Direction.NEGATIVE)) if effect == Direction.QUESTION else \
        {effect} if derivative == Direction.NEUTRAL else {derivative}

# TODO: incorporate transformation based on check_value_correspondence
def next_magnitudes(entity_state: EntityState) -> List[Dict[str, Enum]]:
    state = entity_state.state
    entity = entity_state.entity
    next_magnitudes = {k:
        list(map(lambda x: (k, x),
            {move_magnitude(pair, entity.quantities[k].quantitySpace)} \
            .union(set() if is_point(pair.magnitude) else {pair.magnitude})
        ))
        for k, pair in state.items()
    }
    magnitude_combinations = list(map(dict, itertools.product(*next_magnitudes.values())))
    return magnitude_combinations

def move_magnitude(pair: QuantityPair, space: EnumMeta) -> Enum:
    '''move a magnitude based on its derivative'''
    members = list(space.__members__)
    idx = {k: i for i, k in list(enumerate(members))}[pair.magnitude.name]
    new_idx = min(len(members)-1, max(0, idx + to_sign(pair.derivative)))
    return space[members[new_idx]]

# # TODO: change this from a filter to a transformation
# def check_extremes(entity_state: EntityState) -> bool:
#     '''ensure derivatives are clipped when the magnitudes are at an extreme point'''
#     state = entity_state.state
#     quantities = entity_state.entity.quantities
#     for k, pair in state.items():
#         mag = pair.magnitude
#         der = pair.derivative
#         enum = quantities[k].quantitySpace
#         side = extreme_direction(mag, enum)
#         if is_point(mag) and der == side and der != Direction.NEUTRAL:
#             return False
#     return True

# def extreme_direction(magnitude: Enum, enum: EnumMeta) -> Direction:
#     '''get a direction from a magnitude based on whether it is at the
#        high extreme (positive), low (negative), or in between (neutral).'''
#     val = magnitude.value
#     vals = [mag.value for mag in dict(enum.__members__).values()]
#     return Direction.NEGATIVE if val == min(vals) else \
#            Direction.POSITIVE if val == max(vals) else \
#            Direction.NEUTRAL

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

# TODO: change this from a filter to a transformation
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

def check_not_equal(stateA: EntityState, stateB: EntityState) -> bool:
    '''confirm two states are distinct'''
    return stateA != stateB

def check_transition(a: EntityState, b: EntityState) -> bool:
    '''confirm a source state can transition into a target state'''
    return check_continuous(a, b) and check_point_range(a, b) and check_not_equal(a, b)
