'''qualitative reasoning'''

from enum import Enum, EnumMeta
from typing import List, Dict, Tuple
from qr_types import *

import yaml
import itertools
from prune import *

def make_entity(name: str, quantities: List[Quantity], relations: List[Relationship], exogenous_dict: Dict[str, bool]) -> Entity:
    '''wrap the entity ctor to handle Quantity dict creation'''
    qty_dict = {qty.name: qty for qty in quantities}
    return Entity(name, qty_dict, relations, exogenous_dict)

def make_entity_state(entity: Entity, state_dict: Dict[str, Tuple[Enum, Direction]]) -> EntityState:
    '''wrap the EntityState ctor to handle state dict creation'''
    pair_state = {k: QuantityPair(*tpl) for k, tpl in state_dict.items()}
    return EntityState(entity, pair_state)

def gen_state_graph(entity_state: EntityState) -> StateGraph:
    nodes = {}
    edges = []
    state = entity_state
    k = state_key(state)
    nodes.update({ k: state })
    (nodes, edges) = handle_state(state, nodes, edges, k)  # recursively mutate nodes/edges here

    sg = StateGraph(nodes, edges)
    # TODO: handle exogenous state changes?
    return sg

def handle_state(
    state: EntityState,
    nodes: Dict[str, EntityState],
    edges: List[Tuple[str, str]],
    k: str) -> Tuple[Dict[str, EntityState], List[Tuple[str, str]]]:
    ''' recursively handle a state. impure! mutates nodes/edges to return.'''
    for next_state in next_states(state):
        next_k = state_key(next_state)
        edges.append((k, next_k))
        if not next_k in nodes:
            nodes.update({ next_k: next_state })
            (nodes, edges) = handle_state(next_state, nodes, edges, next_k)
    return (nodes, edges)

def serialize_derivative(derivative: Direction) -> str:
    return {
        Direction.POSITIVE: '+',
        Direction.NEGATIVE: '-',
        Direction.NEUTRAL: '0',
        Direction.QUESTION: '?',
    }[derivative]

def serialize_magnitude(magnitude: Enum) -> str:
    return {
        'ZERO': '0',
        'PLUS': '+',
        'MAX': 'max',
    }.get(magnitude.name, magnitude.name)

def serialize_quantity(k: str) -> str:
    return {
        'volume': 'Vol',
        'inflow': 'In',
        'outflow': 'Out',
        'pressure': 'Pres',
        'height': 'Hi',
    }.get(k, k)

def pretty_print(entity_state: EntityState, idx: int) -> str:
    state = entity_state.state
    # keys = state
    keys = [
        'inflow',
        'volume',
        'outflow',
        'pressure',
        'height',
    ]
    hash = ''.join([f"{serialize_magnitude(state[k].magnitude)}{serialize_derivative(state[k].derivative)}" for k in keys if k in state])
    return f'State {idx}\n{hash}\n' + '\n'.join([f"{serialize_quantity(k)}: ({serialize_magnitude(state[k].magnitude)}, {serialize_derivative(state[k].derivative)})" for k in keys if k in state])

def inter_state_trace(a: EntityState, b: EntityState) -> str:
    '''inter-state trace, showing states and transition validity by the various rules'''
    # potential improvement: show why stuff changed
    continuous = check_continuous(a, b)
    point_range = check_point_range(a, b)
    not_equal = check_not_equal(a, b)
    # valid = check_transition(a, b)
    return yaml.dump({
        # 'magnitude_valid': magnitude,
        # 'derivative_valid': derivative,
        'continuous_valid': continuous,
        'point_range_valid': point_range,
        'not_equal_valid': not_equal,
        # 'transition_valid': valid,
        # 'a': intra_state_trace(a),
        # 'b': intra_state_trace(b),
    })

def serialize_change(derivative: Direction) -> str:
    return {
        Direction.NEUTRAL: 'stay at',
        Direction.POSITIVE: 'go up from',
        Direction.NEGATIVE: 'go down from',
        Direction.QUESTION: 'go any way from',
    }[derivative]

def intra_state_trace(entity_state: EntityState) -> str:
    '''intra-state trace, showing type, validity, and state'''
    # potential improvement: show how things will change (i.e. after adding in question marks?)
    # state = {k: (pair.magnitude.name, pair.derivative.name) for k, pair in entity_state.state.items()}
    derivatives = [f"{serialize_quantity(k)} {'will' if is_point(pair.magnitude) or pair.derivative == Direction.NEUTRAL else 'may'} {serialize_change(pair.derivative)} {serialize_magnitude(pair.magnitude)}" for k, pair in entity_state.state.items()]
    return yaml.dump({
        # 'type': entity_state.entity.name,
        'derivatives': derivatives,
        # 'state': state,
    })

def to_pairs(lst):
    return list(zip(*[lst[x::2] for x in (0, 1)]))

def wrap_enums(qty_vals: Tuple[Quantity, Tuple[int, int]]) -> Tuple[str, QuantityPair]:
    '''wraps enum values back into their enums'''
    (qty, (val, speed)) = qty_vals
    k = qty.name
    magnitude = qty.quantitySpace(val)
    derivative = Direction(speed)
    pair = QuantityPair(magnitude, derivative)
    return (k, pair)
