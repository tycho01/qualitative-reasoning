from qr import *
from container import *
from mock import *
# from graph import *

def test_make_entity():
    entity = make_entity('container', quantities, relations)
    assert entity.quantities['volume'] == Quantity('volume', Volume)

def test_make_entity_state():
    entity_state = make_entity_state(container, container_state)
    assert entity_state.state['volume'] == QuantityPair(Volume.ZERO, Direction.NEUTRAL)

# def test_gen_state_graph():
#     sg = gen_state_graph(container)
#     # assert draw_state_graph(sg)

def test_serialize_state():
    # print(serialize_state(entity_state))
    assert serialize_state(entity_state) == '''inflow: (0, 3)\noutflow: (0, 2)\nvolume: (0, 2)\n'''

def test_state_key():
    # print(state_key(entity_state))
    assert state_key(entity_state) == 'inflow_0_3_outflow_0_2_volume_0_2_'

def test_inter_state_trace():
    # print(inter_state_trace(entity_state, entity_state))
    assert inter_state_trace(entity_state, entity_state) == '''continuous_valid: true\nnot_equal_valid: false\npoint_range_valid: true\n'''

def test_intra_state_trace():
    # print(intra_state_trace(entity_state))
    assert intra_state_trace(entity_state) == '''correspondence_valid: true\nderivatives:\n- Vol will stay at 0\n- In will go up from 0\n- Out will stay at 0\n'''

def test_to_pairs():
    assert to_pairs([1,2,3,4]) == [(1,2),(3,4)]

def test_wrap_enums():
    assert wrap_enums((Quantity('volume', Volume), (0, 2))) == ('volume', QuantityPair(Volume.ZERO, Direction.NEUTRAL))
