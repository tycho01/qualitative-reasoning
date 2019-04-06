from typing import List, Dict, Tuple

# Function to check whether all the direct influences hold
def check_influence(stateA: EntityState, stateB: EntityState) -> bool:
    state = entity_state.state
    relations = entity_state.entity.relations

def check_value_correspondence(entity_state: EntityState) -> bool:
    '''check if a state is deemed valid by its value correspondence rules'''
    state = entity_state.state
    entity = entity_state.entity
    for relation in entity.relations:
        if type(relation) == ValueCorrespondence:
            if not qty_matches(state, relation.a) == qty_matches(state, relation.b):
                return False
    return True

def qty_matches(state: Dict[str, Tuple[Enum, Direction]], qty_val: Tuple[str, Enum]) -> bool:
    '''check if a state quantity matches a given value'''
    (qty_name, val) = qty_val
    (magnitude, derivative) = state[qty_name]
    return val == magnitude

def check_continuous(stateA: EntityState, stateB: EntityState) -> bool:
    # TODO
    pass

def check_validity(entity_states: List[EntityState]) -> bool:
    # TODO
    pass
