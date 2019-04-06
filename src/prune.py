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
        # Retrieving the names of the source and target quantities
        source_quantity_name = relation.a.name
        target_quantity_name = relation.b.name
        source_quantity_magnitude = state1[source_quantity_name][0].value
        source_quantity_direction = state1[source_quantity_name][1].value

        # Create a list for the target quantity if not present in the dictionary
        if target_quantity_name not in target_quantities:
            target_quantities[target_quantity_name] = []
        
        # If it is a direct influence
        if type(relation) == Influence:
            # If it is a positive direct influence
            if relation.correlation.value == RelationDirection.POSITIVE:
                if source_quantity_magnitude > 0:
                    target_quantities[target_quantity_name].append(DerivativeDirection.POSITIVE)
                elif source_quantity_magnitude == 0:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEUTRAL)
                elif source_quantity_magnitude < 0:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEGATIVE)
            # If it is a negative direct influence
            elif relation.correlation.value == RelationDirection.NEGATIVE:
                if source_quantity_magnitude > 0:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEGATIVE)
                elif source_quantity_magnitude == 0:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEUTRAL)
                elif source_quantity_magnitude < 0:
                    target_quantities[target_quantity_name].append(DerivativeDirection.POSITIVE)
        # If it is a proportional influence
        elif type(relation) == Proportional:
            # If it is a positive proportional influence
            if relation.correlation.value == RelationDirection.POSITIVE:
                if source_quantity_direction == DerivativeDirection.POSITIVE:
                    target_quantities[target_quantity_name].append(DerivativeDirection.POSITIVE)
                elif source_quantity_direction == DerivativeDirection.NEUTRAL:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEUTRAL)
                elif source_quantity_direction == DerivativeDirection.NEGATIVE:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEGATIVE)
                elif source_quantity_direction == DerivativeDirection.QUESTION:
                    target_quantities[target_quantity_name].append(DerivativeDirection.QUESTION)
            # If it is a negative proportional influence
            elif relation.correlation.value == RelationDirection.NEGATIVE:
                if source_quantity_direction == DerivativeDirection.POSITIVE:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEGATIVE)
                elif source_quantity_direction == DerivativeDirection.NEUTRAL:
                    target_quantities[target_quantity_name].append(DerivativeDirection.NEUTRAL)
                elif source_quantity_direction == DerivativeDirection.NEGATIVE:
                    target_quantities[target_quantity_name].append(DerivativeDirection.POSITIVE)
                elif source_quantity_direction == DerivativeDirection.QUESTION:
                    target_quantities[target_quantity_name].append(DerivativeDirection.QUESTION)
        
    # Determining the overall derivative direction for the target quantities
    for target_quantity in target_quantities:
        directions = target_quantities[target_quantity]
        if len(set(directions)) == 1:
            if directions[0] == DerivativeDirection.POSITIVE:
                test_state[target_quantity][1] = DerivativeDirection.POSITIVE
            elif directions[0] == DerivativeDirection.NEGATIVE:
                test_state[target_quantity][1] = DerivativeDirection.NEGATIVE
            elif directions[0] == DerivativeDirection.QUESTION:
                test_state[target_quantity][1] = DerivativeDirection.QUESTION
            elif directions[0] == DerivativeDirection.NEUTRAL:
                pass
        elif len(set(directions)) == 2:
            if DerivativeDirection.NEUTRAL in set(directions):
                if DerivativeDirection.POSITIVE in set(directions):
                    test_state[target_quantity][1] = DerivativeDirection.POSITIVE
                elif DerivativeDirection.NEGATIVE in set(directions):
                    test_state[target_quantity][1] = DerivativeDirection.NEGATIVE
                elif DerivativeDirection.QUESTION in set(directions):
                    test_state[target_quantity][1] = DerivativeDirection.QUESTION
            else:
                test_state[target_quantity][1] = DerivativeDirection.QUESTION
        elif len(set(directions)) > 2:
            test_state[target_quantity][1] = DerivativeDirection.QUESTION
    
    # Returning if the destination state is valid or not
    return test_state == state2

def check_value_correspondence(entity_state: EntityState) -> bool:
    '''check if a state is deemed valid by its value correspondence rules'''
    state = entity_state.state
    entity = entity_state.entity
    for relation in entity.relations:
        if type(relation) == ValueCorrespondence:
            if not _qty_matches(state, relation.a) == _qty_matches(state, relation.b):
                return False
    return True

def _qty_matches(state: Dict[str, QuantityPair], qty_pair: Tuple[str, Enum]) -> bool:
    '''check if a state quantity matches a given value'''
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
