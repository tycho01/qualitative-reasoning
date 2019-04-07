from prune import *
from mock import *

def test_next_states():
    assert len(next_states(entity_state))

def test_next_magnitudes():
    assert len(next_magnitudes(entity_state))

def test_zip_pair():
    assert zip_pair(({'volume': Volume.PLUS}, {'volume': Direction.POSITIVE})) == {'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE)}

def test_next_derivatives():
    assert len(next_derivatives(entity_state))

def test_move_derivative():
    assert move_derivative(Direction.POSITIVE, Direction.QUESTION) == set([Direction.POSITIVE, Direction.NEUTRAL])

def test_move_magnitude():
    k = 'volume'
    space = entity_state.entity.quantities[k].quantitySpace
    assert move_magnitude(QuantityPair(Volume.ZERO, Direction.NEUTRAL), space) == Volume.ZERO
    assert move_magnitude(QuantityPair(Volume.ZERO, Direction.POSITIVE), space) == Volume.PLUS

# def test_check_extremes_good():
#     container_state_good = {
#         'volume': (Volume.MAX, Direction.NEUTRAL),
#         'inflow': (Inflow.ZERO, Direction.POSITIVE),
#         'outflow': (Outflow.ZERO, Direction.NEUTRAL),
#     }
#     entity_state_good = make_entity_state(container, container_state_good)
#     assert check_extremes(entity_state_good) == True

# def test_check_extremes_bad():
#     container_state_bad = {
#         'volume': (Volume.MAX, Direction.POSITIVE),  # can't have direction positive
#         'inflow': (Inflow.ZERO, Direction.NEUTRAL),
#         'outflow': (Outflow.ZERO, Direction.NEUTRAL),
#     }
#     entity_state_bad = make_entity_state(container, container_state_bad)
#     assert check_extremes(entity_state_bad) == False

# def test_extreme_direction():
#     assert extreme_direction(Volume.ZERO, Volume) == Direction.NEGATIVE
#     assert extreme_direction(Volume.PLUS, Volume) == Direction.NEUTRAL
#     assert extreme_direction(Volume.MAX, Volume) == Direction.POSITIVE

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
            Influence(   Quantity('volume', Volume), Quantity('outflow', Outflow)),
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

def test_to_sign():
    assert to_sign(Direction.NEUTRAL) == 0
    assert to_sign(Direction.POSITIVE) == 1
    assert to_sign(Direction.NEGATIVE) == -1

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

def test_is_point():
    assert is_point(Volume.ZERO) == True
    assert is_point(Volume.MAX) == True
    assert is_point(Volume.PLUS) == False

def test_check_not_equal():
    assert check_not_equal(entity_state, entity_state) == False
    assert check_not_equal(entity_state, bonus_entity_state) == True

def test_check_transition():
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
    assert check_transition(entity_state_before, entity_state_after) == True
