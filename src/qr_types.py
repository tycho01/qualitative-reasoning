from enum import Enum, EnumMeta
from dataclasses import dataclass
from typing import List, Dict, Tuple

# values for Direction don't follow semantic conventions of quantity spaces (see below)
class Direction(Enum):
    QUESTION = 0  # question mark option to indicate changes in both directions causing an ambiguous change
    NEGATIVE = 1
    NEUTRAL  = 2
    POSITIVE = 3

# for each quantity space we need to know:
# - the order (in which to transition), so ensure the enums are logically ordered!
# - what is negative or positive (needed for influence relation?) - ensure underlying values reflect this!
# - represent point values as even numbers (-> makes 0 a point), ranges as odd numbers.
@dataclass
class Quantity:
    name: str
    quantitySpace: EnumMeta

@dataclass
class Relation:
    pass

@dataclass
class Relationship(Relation):
    a: Quantity
    b: Quantity
    # ^ EnumMeta?

@dataclass
class Influence(Relationship):
     correlation: Direction = Direction.POSITIVE

@dataclass
class Proportional(Relationship):
    correlation: Direction = Direction.POSITIVE

@dataclass
class ValueCorrespondence(Relation):
    '''if a then b. a/b denote (quantity name, enum value)'''
    a: Tuple[str, Enum]
    b: Tuple[str, Enum]

@dataclass
class Entity:
    name: str
    quantities: Dict[str, Quantity]
    relations: List[Relation]
    # ^ out of scope: cross-entity relations

@dataclass
class QuantityPair:
    magnitude: Enum
    derivative: Direction

@dataclass
class EntityState:
    entity: Entity
    state: Dict[str, QuantityPair]

@dataclass
class StateGraph:
    states: Dict[str, EntityState]
    edges: List[Tuple[str, str]]
