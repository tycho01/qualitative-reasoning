# Function to check whether all the direct influences hold
def check_direct_influence(state, relations):

    # Retrieving the involved quantities
    inflow_state = state['inflow']
    volume_state = state['volume']
    outflow_state = state['outflow']

    # Retrieving the magnitude and direction of the quantities
    inflow_mag_state, inflow_dir_state = inflow_state[0].value, inflow_state[1].value
    volume_mag_state, volume_dir_state = volume_state[0].value, volume_state[1].value
    outflow_mag_state, outflow_dir_state = outflow_state[0].value, outflow_state[1].value

def check_proportional_influence(state, relations):
    #TODO

def check_value_correspondence(state, relations):
    #TODO

def check_validity(states, relations):
    #TODO