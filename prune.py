# Importing the Libraries
from qr import *
import copy
from typing import List, Dict, Tuple

# Function to check whether all the influences hold
def check_influence(source_state: EntityState, target_state:EntityState) -> bool:

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
            source_quantity_magnitude = state1[source_quantity_name].magnitude
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
        if len(set(directions)) == 1:
            if directions[0] == Direction.POSITIVE.value:
                test_state[target_quantity][1] = Direction.POSITIVE
            elif directions[0] == Direction.NEGATIVE.value:
                test_state[target_quantity][1] = Direction.NEGATIVE
            elif directions[0] == Direction.QUESTION.value:
                test_state[target_quantity][1] = Direction.QUESTION
            elif directions[0] == Direction.NEUTRAL.value:
                pass
        elif len(set(directions)) == 2:
            if Direction.NEUTRAL.value in set(directions):
                if Direction.POSITIVE.value in set(directions):
                    test_state[target_quantity][1] = Direction.POSITIVE
                elif Direction.NEGATIVE.value in set(directions):
                    test_state[target_quantity][1] = Direction.NEGATIVE
                elif Direction.QUESTION.value in set(directions):
                    test_state[target_quantity][1] = Direction.QUESTION
            else:
                test_state[target_quantity][1] = Direction.QUESTION
        elif len(set(directions)) > 2:
            test_state[target_quantity][1] = Direction.QUESTION
    
    # Returning if the destination state is valid or not
    return test_state == state2

def perform_direct_influence(direct_influence_type: int, source_quantity_magnitude: int) -> int:
    type_sign = -1 if direct_influence_type == RelationDirection.NEGATIVE.value else 1
    source_quantity_magnitude_sign = 1 if source_quantity_magnitude > 0 else 0 if source_quantity_magnitude == 0 else -1
    resulting_sign = type_sign * source_quantity_magnitude_sign
    return Direction.POSITIVE.value if resulting_sign == 1 else Direction.NEUTRAL.value if resulting_sign == 0 else Direction.NEGATIVE.value

def perform_indirect_influence(indirect_influence_type: int, source_quantity_direction: Enum) -> int:
    type_sign = -1 if indirect_influence_type == RelationDirection.NEGATIVE.value else 1
    source_quantity_direction_sign = 1 if source_quantity_direction == Direction.POSITIVE else 0 if source_quantity_direction == Direction.NEUTRAL else -1 if source_quantity_direction == Direction.NEGATIVE else 2
    resulting_sign = type_sign * source_quantity_direction_sign
    return Direction.POSITIVE.value if resulting_sign == 1 else Direction.NEUTRAL.value if resulting_sign == 0 else Direction.NEGATIVE.value if resulting_sign == -1 else Direction.QUESTION.value

def check_value_correspondence(entity_state: EntityState) -> bool:
    '''check if a state is deemed valid by its value correspondence rules'''
    state = entity_state.state
    entity = entity_state.entity
    for relation in entity.relations:
        if type(relation) == ValueCorrespondence:
            if not qty_matches(state, relation.a) == qty_matches(state, relation.b):
                return False
    return True

def qty_matches(state: Dict[str, QuantityPair], qty_pair: Tuple[str, Enum]) -> bool:
    '''check if a state quantity matches a given value'''
    (qty_name, val) = qty_pair
    return val == state[qty_name].magnitude

def check_continuous(stateA: EntityState, stateB: EntityState) -> bool:
    # TODO
    pass
