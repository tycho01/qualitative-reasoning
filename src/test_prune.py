from prune import *
from mock import *

# def test_check_influence_good():
#     container_state_before = {
#         'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
#         'inflow': (Inflow.ZERO, DerivativeDirection.POSITIVE),
#         'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
#     }
#     container_state_after = {
#         'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
#         'inflow': (Inflow.PLUS, DerivativeDirection.POSITIVE),
#         'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
#     }
#     entity_state_before = make_entity_state(container, container_state_before)
#     entity_state_after = make_entity_state(container, container_state_after)
#     assert check_influence(entity_state_before, entity_state_after) == True

# def test_check_influence_bad():
#     container_state_before = {
#         'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
#         'inflow': (Inflow.PLUS, DerivativeDirection.POSITIVE),
#         'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
#     }
#     container_state_after = {
#         'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
#         'inflow': (Inflow.ZERO, DerivativeDirection.POSITIVE),
#         'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
#     }
#     entity_state_before = make_entity_state(container, container_state_before)
#     entity_state_after = make_entity_state(container, container_state_after)
#     assert check_influence(entity_state_before, entity_state_after) == False

def test_check_value_correspondence_good():
    assert check_value_correspondence(entity_state) == True

def test_check_value_correspondence_bad():
    # volume/outflow are tied in zero/max
    container_state_bad = {
        'volume': (Volume.ZERO, DerivativeDirection.NEGATIVE),
        'inflow': (Inflow.ZERO, DerivativeDirection.NEUTRAL),
        'outflow': (Outflow.PLUS, DerivativeDirection.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state_bad)
    assert check_value_correspondence(entity_state_bad) == False

def test_qty_matches():
    state = {'volume': QuantityPair(Volume.ZERO, DerivativeDirection.NEUTRAL)}
    qty_pair = ('volume', Volume.ZERO)
    assert qty_matches(state, qty_pair) == True

def test_check_continuous():
    # good
    container_state_good = {
        'volume': (Volume.ZERO, DerivativeDirection.POSITIVE),
        'inflow': (Inflow.ZERO, DerivativeDirection.NEUTRAL),
        'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
    }
    entity_state_good = make_entity_state(container, container_state_good)
    assert check_continuous(entity_state_good, entity_state) == True
    # bad
    container_state_bad = {
        'volume': (Volume.ZERO, DerivativeDirection.NEGATIVE),
        'inflow': (Inflow.ZERO, DerivativeDirection.NEUTRAL),
        'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state_bad)
    assert check_continuous(entity_state_good, entity_state_bad) == False

def test_check_point_range_good():
    container_state = {
        'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
        'inflow': (Inflow.PLUS, DerivativeDirection.NEUTRAL),  # changed range
        'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
    }
    entity_state_good = make_entity_state(container, container_state)
    assert check_point_range(entity_state_good, entity_state) == True

def test_check_point_range_bad():
    container_state = {
        'volume': (Volume.MAX, DerivativeDirection.NEUTRAL),  # changed point
        'inflow': (Inflow.PLUS, DerivativeDirection.NEUTRAL),  # changed range
        'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state)
    assert check_point_range(entity_state_bad, entity_state) == False

def test_check_not_equal():
    assert check_not_equal(entity_state, entity_state) == False
    assert check_not_equal(entity_state, bonus_entity_state) == True

# def test_can_transition():
#     container_state_before = {
#         'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
#         'inflow': (Inflow.ZERO, DerivativeDirection.POSITIVE),
#         'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
#     }
#     container_state_after = {
#         'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
#         'inflow': (Inflow.PLUS, DerivativeDirection.POSITIVE),
#         'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
#     }
#     entity_state_before = make_entity_state(container, container_state_before)
#     entity_state_after = make_entity_state(container, container_state_after)
#     assert can_transition(entity_state_before, entity_state_after) == True

def test_filter_states():
    container_state_bad = {
        'volume': (Volume.ZERO, DerivativeDirection.NEGATIVE),
        'inflow': (Inflow.ZERO, DerivativeDirection.NEUTRAL),
        'outflow': (Outflow.PLUS, DerivativeDirection.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state_bad)
    assert len(filter_states([entity_state, entity_state_bad])) == 1
