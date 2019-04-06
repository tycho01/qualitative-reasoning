from typing import List, Dict, Tuple

# Function to check whether all the direct influences hold
def check_influence(stateA: EntityState, stateB: EntityState) -> bool:
    state = entity_state.state
    relations = entity_state.entity.relations

    # Retrieving the involved quantities
    inflow_state = state['inflow']
    volume_state = state['volume']
    outflow_state = state['outflow']

    # Retrieving the magnitude and direction of the quantities
    inflow_mag_state, inflow_dir_state = inflow_state[0].value, inflow_state[1].value
    volume_mag_state, volume_dir_state = volume_state[0].value, volume_state[1].value
    outflow_mag_state, outflow_dir_state = outflow_state[0].value, outflow_state[1].value

def check_value_correspondence(entity_state: EntityState) -> bool:
    # TODO
    pass

def check_continuous(stateA: EntityState, stateB: EntityState) -> bool:
    # TODO
    pass

def check_validity(entity_states: List[EntityState]) -> bool:
    # TODO
    pass
