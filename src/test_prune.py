from prune import *
from mock import *

# def test_check_influence_good():
#     container_state_before = {
#         'volume': (Volume.ZERO, Direction.NEUTRAL),
#         'inflow': (Inflow.ZERO, Direction.POSITIVE),
#         'outflow': (Outflow.ZERO, Direction.NEUTRAL),
#     }
#     container_state_after = {
#         'volume': (Volume.ZERO, Direction.NEUTRAL),
#         'inflow': (Inflow.PLUS, Direction.POSITIVE),
#         'outflow': (Outflow.ZERO, Direction.NEUTRAL),
#     }
#     entity_state_before = make_entity_state(container, container_state_before)
#     entity_state_after = make_entity_state(container, container_state_after)
#     assert check_influence(entity_state_before, entity_state_after) == True

def test_check_influence_bad():
    container_state_before = {
        'volume': (Volume.ZERO, Direction.NEUTRAL),
        'inflow': (Inflow.PLUS, Direction.POSITIVE),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    container_state_after = {
        'volume': (Volume.ZERO, Direction.NEUTRAL),
        'inflow': (Inflow.ZERO, Direction.POSITIVE),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_before = make_entity_state(container, container_state_before)
    entity_state_after = make_entity_state(container, container_state_after)
    assert check_influence(entity_state_before, entity_state_after) == False

def test_state_derivatives():
    state = {'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE)}
    assert state_derivatives(state) == {'volume': Direction.POSITIVE}

def test_relation_effects():
    assert relation_effects(
        {
            'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE)
        },
        []
    ) == {'volume': set()}
    assert relation_effects(
        {
            'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE)
        },
        [
            Influence(Quantity('volume', Volume), Quantity('outflow', Outflow))
        ]
    ) == {'volume': set(), 'outflow': {Direction.POSITIVE}}
    assert relation_effects(
        {
            'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE)
        },
        [
            Influence(Quantity('volume', Volume), Quantity('outflow', Outflow)),
            Proportional(Quantity('volume', Volume), Quantity('outflow', Outflow), Direction.NEGATIVE)
        ]) == {'volume': set(), 'outflow': {Direction.POSITIVE, Direction.NEGATIVE}}

def test_combine_derivatives():
    assert combine_derivatives(set()) == Direction.NEUTRAL
    assert combine_derivatives({Direction.POSITIVE}) == Direction.POSITIVE
    assert combine_derivatives({Direction.POSITIVE, Direction.NEGATIVE}) == Direction.QUESTION
    assert combine_derivatives({Direction.NEUTRAL, Direction.NEGATIVE}) == Direction.NEGATIVE

def test_check_value_correspondence_good():
    assert check_value_correspondence(entity_state) == True

def test_check_value_correspondence_bad():
    # volume/outflow are tied in zero/max
    container_state_bad = {
        'volume': (Volume.ZERO, Direction.NEGATIVE),
        'inflow': (Inflow.ZERO, Direction.NEUTRAL),
        'outflow': (Outflow.PLUS, Direction.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state_bad)
    assert check_value_correspondence(entity_state_bad) == False

def test_check_perform_direct_influence():
    assert direct_influence(Direction.POSITIVE, 0) == Direction.NEUTRAL

def test_check_perform_indirect_influence():
    assert indirect_influence(Direction.NEGATIVE, Direction.POSITIVE) == Direction.NEGATIVE

def test_qty_matches():
    state = {'volume': QuantityPair(Volume.ZERO, Direction.NEUTRAL)}
    qty_pair = ('volume', Volume.ZERO)
    assert qty_matches(state, qty_pair) == True

def test_check_magnitude_changes():
    container_state_before = {
        'volume': (Volume.ZERO, Direction.NEUTRAL),
        'inflow': (Inflow.ZERO, Direction.POSITIVE),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    container_state_after = {
        'volume': (Volume.ZERO, Direction.NEUTRAL),
        'inflow': (Inflow.PLUS, Direction.POSITIVE),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_before = make_entity_state(container, container_state_before)
    entity_state_after = make_entity_state(container, container_state_after)
    assert check_magnitude_changes(entity_state_before.state, entity_state_after.state) == {
        'inflow': Direction.POSITIVE,
        'outflow': Direction.NEUTRAL,
        'volume': Direction.NEUTRAL,
    }

def test_num_to_direction():
    assert num_to_direction(0) == Direction.NEUTRAL
    assert num_to_direction(123) == Direction.POSITIVE
    assert num_to_direction(-123) == Direction.NEGATIVE

def test_check_continuous():
    # good
    container_state_good = {
        'volume': (Volume.ZERO, Direction.POSITIVE),
        'inflow': (Inflow.ZERO, Direction.NEUTRAL),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_good = make_entity_state(container, container_state_good)
    assert check_continuous(entity_state_good, entity_state) == True
    # bad
    container_state_bad = {
        'volume': (Volume.ZERO, Direction.NEGATIVE),
        'inflow': (Inflow.ZERO, Direction.NEUTRAL),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state_bad)
    assert check_continuous(entity_state_good, entity_state_bad) == False

def test_check_point_range_good():
    container_state = {
        'volume': (Volume.ZERO, Direction.NEUTRAL),
        'inflow': (Inflow.PLUS, Direction.NEUTRAL),  # changed range
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_good = make_entity_state(container, container_state)
    assert check_point_range(entity_state_good, entity_state) == True

def test_check_point_range_bad():
    container_state = {
        'volume': (Volume.MAX, Direction.NEUTRAL),  # changed point
        'inflow': (Inflow.PLUS, Direction.NEUTRAL),  # changed range
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state)
    assert check_point_range(entity_state_bad, entity_state) == False

def test_check_not_equal():
    assert check_not_equal(entity_state, entity_state) == False
    assert check_not_equal(entity_state, bonus_entity_state) == True

# def test_can_transition():
#     container_state_before = {
#         'volume': (Volume.ZERO, Direction.NEUTRAL),
#         'inflow': (Inflow.ZERO, Direction.POSITIVE),
#         'outflow': (Outflow.ZERO, Direction.NEUTRAL),
#     }
#     container_state_after = {
#         'volume': (Volume.ZERO, Direction.NEUTRAL),
#         'inflow': (Inflow.PLUS, Direction.POSITIVE),
#         'outflow': (Outflow.ZERO, Direction.NEUTRAL),
#     }
#     entity_state_before = make_entity_state(container, container_state_before)
#     entity_state_after = make_entity_state(container, container_state_after)
#     assert can_transition(entity_state_before, entity_state_after) == True

def test_filter_states():
    container_state_bad = {
        'volume': (Volume.ZERO, Direction.NEGATIVE),
        'inflow': (Inflow.ZERO, Direction.NEUTRAL),
        'outflow': (Outflow.PLUS, Direction.NEUTRAL),
    }
    entity_state_bad = make_entity_state(container, container_state_bad)
    assert len(filter_states([entity_state, entity_state_bad])) == 1
