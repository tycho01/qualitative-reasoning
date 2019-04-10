# Importing the Libraries
import numpy as np
import copy
from typing import List, Dict, Tuple, Set
import itertools
from qr_types import *

def next_states(entity_state: EntityState) -> List[EntityState]:
    entity = entity_state.entity
    state = entity_state.state
    magnitudes = next_magnitudes(entity_state)
    tmp_entity_states = list(map(lambda state_dict: EntityState(entity, {k: QuantityPair(magnitude, state[k].derivative) for k, magnitude in state_dict.items()}), magnitudes))
    new_states = [b for a in tmp_entity_states for b in derivative_states(a)]
    return new_states

def derivative_states(a: EntityState) -> List[EntityState]:
    options = []
    for deriv_dict_direct in next_derivatives(a, True):
        state1 = {k: QuantityPair(a.state[k].magnitude, derivative) for k, derivative in deriv_dict_direct.items()}
        b1 = EntityState(a.entity, state1)
        # proportionality_effect_sets = relation_effects(state, a.entity.relations, False)
        for deriv_dict_indirect in next_derivatives(b1, False):
            state2 = {k: QuantityPair(a.state[k].magnitude, derivative) for k, derivative in deriv_dict_direct.items()}
            b2 = EntityState(a.entity, state2)
            if check_transition(a, b2):
                options.append(b2)
    return options

def zip_pair(tpl: Tuple[Dict[str, Enum], Dict[str, Direction]]) -> Dict[str, QuantityPair]:
    (magnitude_dict, derivative_dict) = tpl
    return {k: QuantityPair(magnitude, derivative_dict[k]) for k, magnitude in magnitude_dict.items()}

# TODO: incorporate transformation based on check_extremes
def next_derivatives(entity_state: EntityState, is_direct: bool) -> List[Dict[str, Direction]]:
    entity = entity_state.entity
    relations = entity.relations
    state = entity_state.state
    quantities = entity_state.entity.quantities

    # Dictionary to keep track of the derivative directions of dependent quantities
    effect_sets = relation_effects(state, relations, is_direct)
    # Determine the overall derivative direction for the target quantities
    relation_derivatives = {k: combine_derivatives(directions) for k, directions in effect_sets.items()}
    # check if state2 derivatives are compatible with relation_derivatives:
    next_derivs = {k:
            list(map(
                lambda x: (k, x),
                derivative_options(relation_derivatives[k], quantities[k], pair)
            ))
        for k, pair in state.items()}
    derivative_combinations = list(map(dict, itertools.product(*next_derivs.values())))
    return derivative_combinations

def derivative_options(relation_derivative: Direction, qty: Quantity, pair: QuantityPair) -> Set[Direction]:
    '''check the next possible derivatives based on the extremity check and relationships'''
    magnitude = pair.magnitude
    deriv = pair.derivative
    enum = qty.quantitySpace
    side = extreme_direction(magnitude, enum)
    # if the derivative would push us off the edge the derivative is now neutralized
    if deriv == side and side != Direction.NEUTRAL and is_point(magnitude):
        return {Direction.NEUTRAL}
    else:
        # otherwise return the derivative as altered by any relationships
        return {deriv}.union(move_derivative(deriv, relation_derivative))

def extreme_direction(magnitude: Enum, enum: EnumMeta) -> Direction:
    '''get a direction from a magnitude based on whether it is at the
       high extreme (positive), low (negative), or in between (neutral).'''
    val = magnitude.value
    vals = [mag.value for mag in dict(enum.__members__).values()]
    return Direction.NEGATIVE if val == min(vals) else \
           Direction.POSITIVE if val == max(vals) else \
           Direction.NEUTRAL

def move_derivative(derivative: Direction, effect: Direction) -> Set[Direction]:
    return {Direction.NEUTRAL} if {derivative, effect} == {Direction.POSITIVE, Direction.NEGATIVE} else \
        set([derivative]).union(move_derivative(derivative, Direction.POSITIVE)).union(move_derivative(derivative, Direction.NEGATIVE)) if effect == Direction.QUESTION else \
        {effect} if derivative == Direction.NEUTRAL else {derivative}

def next_magnitudes(entity_state: EntityState) -> List[Dict[str, Enum]]:
    state = entity_state.state
    entity = entity_state.entity

    # get value correspondence requirements per quantity
    reqs = correspondence_reqs(entity_state)
    has_clashes = max(map(len, reqs.values())) > 1
    if has_clashes:
        return set()
    # req_vals = {k: v for k, v in reqs.items() if v}
    req_vals = dict(reqs)

    magnitudes = {k:
        list(map(lambda x: (k, x), magnitude_options(req_vals[k], pair, entity.quantities[k].quantitySpace)))
        for k, pair in state.items()
    }
    magnitude_combinations = list(map(dict, itertools.product(*magnitudes.values())))
    return magnitude_combinations

def magnitude_options(reqs: Dict[str, Set[Enum]], pair: QuantityPair, space: EnumMeta) -> Set[Enum]:
    '''check the next possible magnitudes based on the point/interval check and current derivatives'''
    point_range = set() if is_point(pair.magnitude) else {pair.magnitude}
    rest = {move_magnitude(pair, space)}.union(point_range)
    # filtering approach: no forcing values in a direction
    # return rest.intersection(reqs) if reqs else rest
    # forcing approach: force the quantity to the value in spite of its derivative and point/range priorities
    return reqs if reqs else rest

def correspondence_reqs(entity_state: EntityState) -> Dict[str, Set[Enum]]:
    '''get a dictionary of value correspondence requirements on quantities'''
    entity = entity_state.entity
    state = entity_state.state
    reqs = {k: set() for k in state}
    for relation in entity.relations:
        if type(relation) == ValueCorrespondence and qty_matches(state, relation.a):
            (k, magnitude) = relation.b
            reqs[k].add(magnitude)
    return reqs

def move_magnitude(pair: QuantityPair, space: EnumMeta) -> Enum:
    '''move a magnitude based on its derivative'''
    members = list(space.__members__)
    idx = {k: i for i, k in list(enumerate(members))}[pair.magnitude.name]
    new_idx = min(len(members)-1, max(0, idx + to_sign(pair.derivative)))
    return space[members[new_idx]]

def relation_effects(state: Dict[str, QuantityPair], relations: List[Relation], is_direct: bool) -> Dict[str, Set[Direction]]:
    '''for each quantity in a state find the effects of the relationships working on that quantity'''
    target_quantities = {k: set() for k in state}
    for relation in relations:
        if type(relation) == (Influence if is_direct else Proportional):
            target_k = relation.b.name
            qty1 = state[relation.a.name]
            correl = relation.correlation
            # add the derivative direction
            target_quantities[target_k].add(
                direct_influence(correl, qty1.magnitude.value)
                if is_direct else
                indirect_influence(correl, qty1.derivative)
            )
    return target_quantities

def combine_derivatives(directions_: Set[Direction]) -> Direction:
    '''obtain a Direction by combining a set of them. this may give Direction.QUESTION.'''
    directions = directions_ - {Direction.NEUTRAL}
    size = len(set(directions))
    return Direction.NEUTRAL if size == 0 else list(directions)[0] if size == 1 else Direction.QUESTION

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

def to_sign(direction: Enum) -> int:
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

def simulate_exogeneous_behaviour(a : EntityState) -> Direction:
    # Output
    exogenous_inflow_derivative = None

    # Extracting the Inflow Quantity
    a_inflow_derivative = a.state['inflow'].derivative
    
    # Simulating the random exogenous behaviour satisfying the continuity constraint
    if a_inflow_derivative == Direction.NEGATIVE:
        exogenous_inflow_derivative = np.random.choice([Direction.NEGATIVE, Direction.NEUTRAL])
    elif a_inflow_derivative == Direction.NEUTRAL:
        exogenous_inflow_derivative = np.random.choice([Direction.NEGATIVE, Direction.NEUTRAL, Direction.POSITIVE])
    elif a_inflow_derivative == Direction.POSITIVE:
        exogenous_inflow_derivative = np.random.choice([Direction.POSITIVE, Direction.NEUTRAL])
    
    # Return the Exogenous Derivative
    return exogenous_inflow_derivative

