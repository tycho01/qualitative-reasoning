from qr import *
from container import *
from mock import *
# from graph import *

def test_make_entity():
    entity = make_entity('container', quantities, relations)
    assert entity.quantities['volume'] == Quantity('volume', Volume)

def test_make_entity_state():
    entity_state = make_entity_state(container, container_state)
    assert entity_state.state['volume'] == QuantityPair(Volume.ZERO, DerivativeDirection.NEUTRAL)

# def test_gen_state_graph():
#     sg = gen_state_graph(container)
#     # assert draw_state_graph(sg)

def test_serialize_state():
    assert serialize_state(entity_state) == "{'volume': (0, 2), 'inflow': (0, 2), 'outflow': (0, 2)}"

def test_inter_state_trace():
    assert inter_state_trace(entity_state, entity_state) == None

def test_intra_state_trace():
    assert intra_state_trace(entity_state) == "{'volume': ('ZERO', 'NEUTRAL'), 'inflow': ('ZERO', 'NEUTRAL'), 'outflow': ('ZERO', 'NEUTRAL')}"

def test_to_pairs():
    assert to_pairs([1,2,3,4]) == [(1,2),(3,4)]

def test_wrap_enums():
    assert wrap_enums((Quantity('volume', Volume), (0, 2))) == ('volume', QuantityPair(Volume.ZERO, DerivativeDirection.NEUTRAL))

def test_gen_states():
    assert len(gen_states(container)) == 1152
