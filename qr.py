'''qualitative reasoning'''

from enum import Enum, EnumMeta
from typing import List, Dict, Tuple
from qr_types import *
from prune import *
import itertools

def make_entity(name: str, quantities: List[Quantity], relations: List[Relationship]) -> Entity:
    '''wrap the entity ctor to handle Quantity dict creation'''
    qty_dict = {qty.name: qty for qty in quantities}
    return Entity(name, qty_dict, relations)

def make_entity_state(entity: Entity, state_dict: Dict[str, Tuple[Enum, DerivativeDirection]]) -> EntityState:
    pair_state = {k: QuantityPair(*tpl) for k, tpl in state_dict.items()}
    return EntityState(entity, pair_state)

def gen_state_graph(entity: Entity) -> StateGraph:
    # generate all possible states
    all_states = gen_states(entity)

    # - see which lead to conflicts based on rules like VC to filter out invalid states/transitions
    possible_states = filter_states(all_states)

    # TODO:
    # - see how they connect, generating edges using Influence/Proportional relationships
    #   - given multiple relationships, first see how these would interact, then apply the result on a state
    #   - point (0, max?, delta 0) vs. range (+, delta -/+) values: points change first.

    states = {}
    edges = []
    state = possible_states[0]
    k = serialize_state(state)
    states.update({ k: state })
    handle_state(state, states, edges)  # recursively mutate states/edges here
    sg = StateGraph(states, edges)
    return sg

def handle_state(
    state: EntityState,
    states: Dict[str, EntityState],
    edges: List[Tuple[str, str]]) -> None:
    ''' recursively handle a state. impure!
        mutates states/edges to return. TODO: change this?
    '''
    for next_state in next_states(state):
        next_k = serialize_state(next_state)
        edges.append((k, next_k))
        if not state in states:
            states.add(state)
            handle_state(next_state, states, edges)

def inter_state_trace(a: EntityState, b: EntityState) -> str:
    # here we can mention intra-state rules like value correspondence
    # TODO: implement
    pass

def intra_state_trace(state: EntityState) -> str:
    # here we can mention intra-state rules like value correspondence
    return str(state)

def to_pairs(lst):
    return list(zip(*[lst[x::2] for x in (0, 1)]))

def wrap_enums(qty_vals: Tuple[Quantity, Tuple[int, int]]) -> Tuple[str, QuantityPair]:
    '''wraps enum values back into their enums'''
    (qty, (val, speed)) = qty_vals
    k = qty.name
    magnitude = qty.quantitySpace(val)
    derivative = DerivativeDirection(speed)
    pair = QuantityPair(magnitude, derivative)
    return (k, pair)

def gen_states(entity: Entity) -> List[EntityState]:
    iterables = list(itertools.chain.from_iterable([
        [
            # magnitudes
            [enumVal.value for enumVal in qty.quantitySpace],
            # derivatives
            [enumVal.value for enumVal in DerivativeDirection]
        ] for qty in entity.quantities.values()
    ]))
    # state_dict: Dict[str, QuantityPair]
    state_dicts = [
        {
            k: QuantityPair(*tpl)
            for k, tpl in map(wrap_enums, zip(entity.quantities.values(), to_pairs(pair)))
        }
        for pair in itertools.product(*iterables)
    ]
    states = [make_entity_state(entity, state_dict) for state_dict in state_dicts]
    return states
