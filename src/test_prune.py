from frozen import FrozenDict
from prune import *
from mock import *

def test_next_states():
    # print(next_states(entity_state))
    assert next_states(entity_state) == {
        # EntityState(container, {
        #     'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE),
        #     'inflow': QuantityPair(Inflow.PLUS, Direction.NEUTRAL),
        #     'outflow': QuantityPair(Outflow.ZERO, Direction.POSITIVE),
        # }),
        EntityState(container, {
            'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.ZERO, Direction.POSITIVE),
        }),
    }

def test_next_states_3():
    es = EntityState(container, {
        'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE),
        'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
        'outflow': QuantityPair(Outflow.ZERO, Direction.POSITIVE),
    })
    # print(next_states(es))
    res = next_states(es)
    assert res == {
        EntityState(container, {
            'volume': QuantityPair(Volume.PLUS, Direction.NEUTRAL),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE),
        }),
        EntityState(container, {
            'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE),
        }),
    }
    # State 3: ++++0+, should be all +

def test_next_magnitudes_3():
    es = EntityState(container, {
        'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE),
        'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
        'outflow': QuantityPair(Outflow.ZERO, Direction.POSITIVE),
    })
    # print(next_magnitudes(es))
    res = next_magnitudes(es)
    assert len(res) == 1
    assert list(res)[0]._d == {
        'inflow': Inflow.PLUS,
        'outflow': Outflow.PLUS,
        'volume': Volume.PLUS,
    }
    # State 3: ++++0+, should be all +

def test_next_states_5():
    es = EntityState(container, {
        'volume': QuantityPair(Volume.PLUS, Direction.NEUTRAL),
        'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
        'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE),
    })
    # print(next_states(es))
    assert next_states(es) == {
        EntityState(container, {
            'volume': QuantityPair(Volume.PLUS, Direction.NEGATIVE),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.PLUS, Direction.NEUTRAL),
        }),
        EntityState(container, {
            'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.MAX, Direction.NEUTRAL),
        }),
        EntityState(container, {
            'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE),
        }),
        EntityState(container, {
            'volume': QuantityPair(Volume.PLUS, Direction.NEUTRAL),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.MAX, Direction.NEUTRAL),
        }),
    }
    # State 5: ++++max+, should have last one 0

def test_derivative_states():

    es = EntityState(container, {
        'volume': QuantityPair(Volume.ZERO, Direction.NEUTRAL),
        'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
        'outflow': QuantityPair(Outflow.ZERO, Direction.NEUTRAL),
    })
    assert derivative_states(es, es) == {
        EntityState(container, {
            'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE),
            'inflow': QuantityPair(Inflow.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.ZERO, Direction.POSITIVE),
        }),
    }

def test_next_magnitudes():
    assert next_magnitudes(entity_state) == {
        FrozenDict({
            'inflow': Inflow.PLUS,
            'outflow': Outflow.ZERO,
            'volume': Volume.ZERO,
        }),
    }

    entity_state_1 = EntityState(container, {
        'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE),
        'inflow': QuantityPair(Inflow.ZERO, Direction.NEUTRAL),
        'outflow': QuantityPair(Outflow.ZERO, Direction.NEUTRAL),
    })

    assert next_magnitudes(entity_state_1) == {
        FrozenDict({
            'inflow': Inflow.ZERO,
            'outflow': Outflow.ZERO,
            'volume': Volume.PLUS,  # Volume can go up
        }),
    }

    entity_state_2 = EntityState(container, {
        'volume': QuantityPair(Volume.ZERO, Direction.NEUTRAL),
        'inflow': QuantityPair(Inflow.ZERO, Direction.NEUTRAL),
        'outflow': QuantityPair(Outflow.ZERO, Direction.POSITIVE),
    })

    assert next_magnitudes(entity_state_2) == {
        FrozenDict({
            'inflow': Inflow.ZERO,
            'outflow': Outflow.ZERO,  # outflow cannot go up due to ValueCorrespondence from Volume.ZERO
            'volume': Volume.ZERO,
        }),
    }

def test_next_magnitudes_point_interval():
    container_state_point = {
        'volume': (Volume.ZERO, Direction.POSITIVE),
        'inflow': (Inflow.PLUS, Direction.POSITIVE),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_point = make_entity_state(container, container_state_point)
    assert next_magnitudes(entity_state_point) == {
        # points move before ranges
        FrozenDict({
            'volume': Volume.PLUS,
            'inflow': Inflow.PLUS,
            'outflow': Outflow.ZERO,
        }),
    }

def test_zip_pair():
    assert zip_pair(({'volume': Volume.PLUS}, {'volume': Direction.POSITIVE})) == {'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE)}

def test_next_derivatives_direct():
    effects = relation_effects(entity_state.state, container.relations, True)
    assert next_derivatives(entity_state, effects) == {
        FrozenDict({
            'volume': Direction.NEUTRAL,
            'inflow': Direction.POSITIVE,
            'outflow': Direction.NEUTRAL,
        }),
    }

def test_next_derivatives_indirect():
    effects = relation_effects(entity_state.state, container.relations, False)
    assert next_derivatives(entity_state, effects) == {
        FrozenDict({
            'volume': Direction.NEUTRAL,
            'inflow': Direction.POSITIVE,
            'outflow': Direction.NEUTRAL,
        }),
    }

def test_next_derivatives_clipping():
    container_state_clip = {
        'volume': (Volume.MAX, Direction.POSITIVE),
        'inflow': (Inflow.ZERO, Direction.NEUTRAL),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_clip = make_entity_state(container, container_state_clip)

    effects = relation_effects(entity_state_clip.state, container.relations, True)
    assert next_derivatives(entity_state_clip, effects) == {
        FrozenDict({
            'volume': Direction.NEUTRAL,
            'inflow': Direction.NEUTRAL,
            'outflow': Direction.NEUTRAL,
        }),
    }

    effects = relation_effects(entity_state_clip.state, container.relations, False)
    assert next_derivatives(entity_state_clip, effects) == {
        FrozenDict({
            # volume direction forced to neutral by the extremity check
            'volume': Direction.NEUTRAL,
            'inflow': Direction.NEUTRAL,
            'outflow': Direction.POSITIVE,
        }),
    }

def test_next_derivatives_influence():

    entity_state_1 = EntityState(container, {
        'volume': QuantityPair(Volume.ZERO, Direction.NEUTRAL),
        'inflow': QuantityPair(Inflow.PLUS, Direction.NEUTRAL),
        'outflow': QuantityPair(Outflow.ZERO, Direction.NEUTRAL),
    })

    effects = relation_effects(entity_state_1.state, container.relations, True)
    assert next_derivatives(entity_state_1, effects) == {
        FrozenDict({
            'volume': Direction.POSITIVE,
            'inflow': Direction.NEUTRAL,
            'outflow': Direction.NEUTRAL,
        }),
    }

def test_clip_extremes():
    qty = Quantity('outflow', Outflow)
    pair = QuantityPair(Outflow.MAX, Direction.POSITIVE)
    print(clip_extremes(qty, pair))
    assert clip_extremes(qty, pair) == Direction.NEUTRAL

def test_correspondence_reqs():
    assert correspondence_reqs(entity_state) == {
        'volume': set(),
        'inflow': set(),
        'outflow': {Outflow.ZERO},
    }

    container_state_clip = {
        'volume': (Volume.MAX, Direction.POSITIVE),
        'inflow': (Inflow.ZERO, Direction.NEUTRAL),
        'outflow': (Outflow.ZERO, Direction.NEUTRAL),
    }
    entity_state_clip = make_entity_state(container, container_state_clip)
    assert correspondence_reqs(entity_state_clip) == {
        'volume': set(),
        'inflow': set(),
        'outflow': {Outflow.MAX},
    }

def test_move_derivative():
    assert move_derivative(Direction.POSITIVE, Direction.QUESTION) == set([Direction.POSITIVE, Direction.NEUTRAL])

def test_move_magnitude():
    k = 'volume'
    space = entity_state.entity.quantities[k].quantitySpace
    assert move_magnitude(QuantityPair(Volume.ZERO, Direction.NEUTRAL), space) == Volume.ZERO
    assert move_magnitude(QuantityPair(Volume.ZERO, Direction.POSITIVE), space) == Volume.PLUS

def test_relation_effects():
    assert relation_effects(
        {
            'volume': QuantityPair(Volume.ZERO, Direction.POSITIVE)
        },
        []
        , False
    ) == {'volume': set()}

    assert relation_effects(
        {
            'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE),
            'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE)
        },
        [
            Influence(Quantity('volume', Volume), Quantity('outflow', Outflow))
        ]
        , True
    ) == {'volume': set(), 'outflow': {Direction.POSITIVE}}

    state = {
        'volume': QuantityPair(Volume.PLUS, Direction.POSITIVE),
        'outflow': QuantityPair(Outflow.PLUS, Direction.POSITIVE)
    }
    relations = [
        Influence(   Quantity('volume', Volume), Quantity('outflow', Outflow)),
        Proportional(Quantity('volume', Volume), Quantity('outflow', Outflow), Direction.NEGATIVE)
    ]
    assert relation_effects(state, relations, False) == {'volume': set(), 'outflow': {Direction.NEGATIVE}}
    assert relation_effects(state, relations, True) == {'volume': set(), 'outflow': {Direction.POSITIVE}}

def test_combine_derivatives():
    assert combine_derivatives(set()) == Direction.NEUTRAL
    assert combine_derivatives({Direction.POSITIVE}) == Direction.POSITIVE
    assert combine_derivatives({Direction.POSITIVE, Direction.NEGATIVE}) == Direction.QUESTION
    assert combine_derivatives({Direction.NEUTRAL, Direction.NEGATIVE}) == Direction.NEGATIVE

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
