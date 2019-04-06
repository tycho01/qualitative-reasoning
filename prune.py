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
                    target_quantities[target_quantity_name].append(Direction.POSITIVE)
                elif source_quantity_magnitude == 0:
                    target_quantities[target_quantity_name].append(Direction.NEUTRAL)
                elif source_quantity_magnitude < 0:
                    target_quantities[target_quantity_name].append(Direction.NEGATIVE)
            # If it is a negative direct influence
            elif relation.correlation.value == RelationDirection.NEGATIVE:
                if source_quantity_magnitude > 0:
                    target_quantities[target_quantity_name].append(Direction.NEGATIVE)
                elif source_quantity_magnitude == 0:
                    target_quantities[target_quantity_name].append(Direction.NEUTRAL)
                elif source_quantity_magnitude < 0:
                    target_quantities[target_quantity_name].append(Direction.POSITIVE)
        # If it is a proportional influence
        elif type(relation) == Proportional:
            # If it is a positive proportional influence
            if relation.correlation.value == RelationDirection.POSITIVE:
                if source_quantity_direction == Direction.POSITIVE:
                    target_quantities[target_quantity_name].append(Direction.POSITIVE)
                elif source_quantity_direction == Direction.NEUTRAL:
                    target_quantities[target_quantity_name].append(Direction.NEUTRAL)
                elif source_quantity_direction == Direction.NEGATIVE:
                    target_quantities[target_quantity_name].append(Direction.NEGATIVE)
                elif source_quantity_direction == Direction.QUESTION:
                    target_quantities[target_quantity_name].append(Direction.QUESTION)
            # If it is a negative proportional influence
            elif relation.correlation.value == RelationDirection.NEGATIVE:
                if source_quantity_direction == Direction.POSITIVE:
                    target_quantities[target_quantity_name].append(Direction.NEGATIVE)
                elif source_quantity_direction == Direction.NEUTRAL:
                    target_quantities[target_quantity_name].append(Direction.NEUTRAL)
                elif source_quantity_direction == Direction.NEGATIVE:
                    target_quantities[target_quantity_name].append(Direction.POSITIVE)
                elif source_quantity_direction == Direction.QUESTION:
                    target_quantities[target_quantity_name].append(Direction.QUESTION)
        
    # Determining the overall derivative direction for the target quantities
    for target_quantity in target_quantities:
        directions = target_quantities[target_quantity]
        if len(set(directions)) == 1:
            if directions[0] == Direction.POSITIVE:
                test_state[target_quantity][1] = Direction.POSITIVE
            elif directions[0] == Direction.NEGATIVE:
                test_state[target_quantity][1] = Direction.NEGATIVE
            elif directions[0] == Direction.QUESTION:
                test_state[target_quantity][1] = Direction.QUESTION
            elif directions[0] == Direction.NEUTRAL:
                pass
        elif len(set(directions)) == 2:
            if Direction.NEUTRAL in set(directions):
                if Direction.POSITIVE in set(directions):
                    test_state[target_quantity][1] = Direction.POSITIVE
                elif Direction.NEGATIVE in set(directions):
                    test_state[target_quantity][1] = Direction.NEGATIVE
                elif Direction.QUESTION in set(directions):
                    test_state[target_quantity][1] = Direction.QUESTION
            else:
                test_state[target_quantity][1] = Direction.QUESTION
        elif len(set(directions)) > 2:
            test_state[target_quantity][1] = Direction.QUESTION
    
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

def qty_matches(state: Dict[str, QuantityPair], qty_pair: Tuple[str, Enum]) -> bool:
    '''check if a state quantity matches a given value'''
    (qty_name, val) = qty_pair
    return val == state[qty_name].magnitude

def check_continuous(stateA: EntityState, stateB: EntityState) -> bool:
    # TODO
    pass

def check_validity(entity_states: List[EntityState]) -> bool:
    # TODO
    pass
