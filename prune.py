# Function to check whether all the direct influences hold
def check_direct_influence(state1, state2, relations):

    # Retrieving the involved quantities
    inflow_state1 = state1['inflow']
    volume_state1 = state1['volume']
    outflow_state1 = state1['outflow']

    # Retrieving the magnitude and direction of the quantities
    inflow_mag_state1, inflow_dir_state1 = inflow_state1[0].value, inflow_state1[1].value
    volume_mag_state1, volume_dir_state1 = volume_state1[0].value, volume_state1[1].value
    outflow_mag_state1, outflow_dir_state1 = outflow_state1[0].value, outflow_state1[1].value

def check_proportional_influence(state, relations):
    #TODO

def check_value_correspondence(state, relations):
    #TODO

def check_validity(states, relations):
    #TODO