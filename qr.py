'''qualitative reasoning'''

from enum import Enum, EnumMeta
from dataclasses import dataclass
from typing import List, Dict, Tuple

class Direction(Enum):
  QUESTION = 0  # question mark option to indicate changes in both directions causing an ambiguous change
  NEGATIVE = 1
  NEUTRAL  = 2
  POSITIVE = 3

class RelationDirection(Enum):
  NEGATIVE = 1
  POSITIVE = 2

# class RelationType(Enum):
#   PROPORTIONAL = 1  # pos: d B pos if d A pos
#   INFLUENCE    = 2  # pos: d B pos if   A pos

# for each quantity space we need to know:
# - the order (in which to transition), so ensure the enums are logically ordered!
# - what is negative or positive (needed for influence relation?) - ensure underlying values reflect this!
# - represent point values as even numbers (-> makes 0 a point), ranges as odd numbers.
@dataclass
class Quantity:
  name: str
  quantitySpace: EnumMeta
  # TODO: figure out how to factor above vs. below fields
  # qty: str
  # change: Direction

@dataclass
class Relationship:
  a: Quantity
  b: Quantity
  # ^ EnumMeta?

@dataclass
class Influence(Relationship):
  correlation: RelationDirection = RelationDirection.POSITIVE

@dataclass
class Proportional(Relationship):
  correlation: RelationDirection = RelationDirection.POSITIVE

# class EqualityRelation(Enum):
#     LTE = 1
#     LT = 2
#     EQ = 3
#     GT = 4
#     GTE = 5

# @dataclass
# class Inequality(Relationship):
#     equality: EqualityRelation = EqualityRelation.EQ

@dataclass
class ValueCorrespondence:
    '''if a then b'''
    # TODO: do I need EnumMeta?
    a: Enum
    b: Enum

# @dataclass
# class Addition(Relationship):
#     c: Quantity

# @dataclass
# class Subtraction(Relationship):
#     c: Quantity

@dataclass
class Entity:
  name: str
  quantities: List[Quantity]
  relations: List[Relationship]
  # TODO: ^ is this right, or could a relation be between quantities not part of the same entity? probably not relevant as I think we're only dealing with a single entity here.

@dataclass
class EntityState:
  entity: Entity
  state: Dict[str, Tuple[Enum, Direction]]


@dataclass
class State:
  entities: Dict[str, EntityState]

@dataclass
class StateGraph:
  states: Dict[str, State]
  edges: List[Tuple[str, str]]

# functions

def gen_state_graph(init_state):
  i = 0
  edges = []
  states = {}
  state = init_state
  k = serialize_state(state)
  states.update({ k: state })
  handle_state(state)
  sg = StateGraph(states, edges)
  return sg

# impure!
def handle_state(state, states, edges):
    for next_state in gen_states(state):
        next_k = serialize_state(next_state)
        edges.append((k, next_k))
        if not state in states:
            states.add(state)
            handle_state(next_state)

def serialize_state(state):
    return str(state)

# TODO: adjust this, as we can generate without initial state by itertools.product,
# then filter out invalid states/transitions, then plug in initial state to see
# from where to where we'll go.

# TODO:
# - generate states
# - see which lead to conflicts based on rules like VC
# - see how they connect, generating edges using Influence/Proportional relationships
#   - given multiple relationships, first see how these would interact, then apply the result on a state
#   - point (0, max?, delta 0) vs. range (+, delta -/+) values: points change first.
# - see which states you can reach from initial state

def gen_states(state):
  for k, entity_state in state.entities.items():
      entity = entity_state.entity
      state_ = entity_state.state
      for qty_name, tpl in state_.items():
          qty, change = tpl
          #
          print(qty_name, qty, change)
      name = entity.name
      quantities = entity.quantities
      for qty in quantities:
          #
          print(qty)
      relations = entity.relations
      for relation in relations:
        a = relation.a
        b = relation.b
        print(relation, a, b)
        clz = type(relation)
        if clz == ValueCorrespondence:
        # elif clz == Influence:
        # elif clz == Proportional:
          pass
        else:
          # throw Error
          correlation = relation.correlation
