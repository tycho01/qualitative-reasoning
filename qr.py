'''qualitative reasoning'''

from enum import Enum, EnumMeta
from dataclasses import dataclass
from typing import List

class Direction(Enum):
  NEGATIVE = 1
  NEUTRAL  = 2
  POSITIVE = 3

class RelationType(Enum):
  PROPORTIONAL = 1  # pos: d B pos if d A pos
  INFLUENCE    = 2  # pos: d B pos if   A pos

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
  relationType: RelationType
  correlation: Direction

# TODO: inequalities, subtraction

@dataclass
class VC:
    # TODO: idk wtf VC stands for. also do I need EnumMeta?
    a: Enum
    b: Enum

@dataclass
class Entity:
  name: str
  quantities: List<Quantity>
  relations: List<Relationship>

@dataclass
class State:
  entities: List<Entity>

class StateGraph:
  # TODO: ???
  states: List<State>
