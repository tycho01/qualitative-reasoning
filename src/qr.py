'''qualitative reasoning'''

from enum import Enum, EnumMeta
from typing import List, Dict, Tuple
from qr_types import *

import re
import itertools
from prune import *

def make_entity(name: str, quantities: List[Quantity], relations: List[Relationship]) -> Entity:
    '''wrap the entity ctor to handle Quantity dict creation'''
    qty_dict = {qty.name: qty for qty in quantities}
    return Entity(name, qty_dict, relations)

def make_entity_state(entity: Entity, state_dict: Dict[str, Tuple[Enum, DerivativeDirection]]) -> EntityState:
    '''wrap the EntityState ctor to handle state dict creation'''
    pair_state = {k: QuantityPair(*tpl) for k, tpl in state_dict.items()}
    return EntityState(entity, pair_state)

def gen_state_graph(entity: Entity) -> StateGraph:
    # generate all possible states
    all_states = gen_states(entity)

    # - see which lead to conflicts based on rules like VC to filter out invalid states/transitions
    possible_states = filter_states(all_states)

    # - see how they connect, generating edges using Influence/Proportional relationships
    #   - given multiple relationships, first see how these would interact, then apply the result on a state
    #   - point (0, max?, delta 0) vs. range (+, delta -/+) values: points change first.
    all_combinations = itertools.product(possible_states, possible_states)
    possible_combinations = list(filter(lambda tpl: can_transition(tpl[0], tpl[1]), all_combinations))

    nodes = {state_key(state): state for state in possible_states}
    edges = [(state_key(pair[0]), state_key(pair[1])) for pair in possible_combinations]

    # nodes = {}
    # edges = []
    # state = possible_states[0]
    # k = state_key(state)
    # nodes.update({ k: state })
    # handle_state(state, nodes, edges)  # recursively mutate nodes/edges here

    sg = StateGraph(nodes, edges)
    return sg

# def handle_state(
#     state: EntityState,
#     states: Dict[str, EntityState],
#     edges: List[Tuple[str, str]]) -> None:
#     ''' recursively handle a state. impure!
#         mutates states/edges to return. TODO: change this?
#     '''
#     for next_state in next_states(state):
#         next_k = state_key(next_state)
#         edges.append((k, next_k))
#         if not state in states:
#             states.add(state)
#             handle_state(next_state, states, edges)

def serialize_state(state: EntityState) -> str:
    '''simple serialization method for EntityState'''
    return str({k: (pair.magnitude.value, pair.derivative.value) for k, pair in state.state.items()})

def state_key(state: EntityState) -> str:
    '''serialize state for graph key purposes'''
    return re.sub(r"[^\w]+", '_', serialize_state(state))

def inter_state_trace(a: EntityState, b: EntityState) -> str:
    # TODO: here we can mention intra-state validity like can_transition
    # TODO: implement
    pass

def intra_state_trace(state: EntityState) -> str:
    # TODO: here we can mention intra-state validity like value correspondence
    # TODO: show how things will change (i.e. after adding in question marks as per check_influence?)
    return str({k: (pair.magnitude.name, pair.derivative.name) for k, pair in state.state.items()})

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
            k: qty_pair
            for k, qty_pair in map(wrap_enums, zip(entity.quantities.values(), to_pairs(pair)))
        }
        for pair in itertools.product(*iterables)
    ]
    states = [EntityState(entity, state_dict) for state_dict in state_dicts]
    return states
