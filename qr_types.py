from enum import Enum, EnumMeta
from dataclasses import dataclass
from typing import List, Dict, Tuple

class DerivativeDirection(Enum):
    QUESTION = 0  # question mark option to indicate changes in both directions causing an ambiguous change
    NEGATIVE = 1  # TODO: should this be represented as negative?
    NEUTRAL  = 2  # TODO: should this be represented as zero?
    POSITIVE = 3

class RelationDirection(Enum):
    NEGATIVE = 1
    POSITIVE = 2

# for each quantity space we need to know:
# - the order (in which to transition), so ensure the enums are logically ordered!
# - what is negative or positive (needed for influence relation?) - ensure underlying values reflect this!
# - represent point values as even numbers (-> makes 0 a point), ranges as odd numbers.
@dataclass
class Quantity:
    name: str
    quantitySpace: EnumMeta

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

@dataclass
class ValueCorrespondence:
    '''if a then b. a/b denote (quantity name, enum value)'''
    a: Tuple[str, Enum]
    b: Tuple[str, Enum]

@dataclass
class Entity:
    name: str
    quantities: Dict[str, Quantity]
    relations: List[Relationship]
    # ^ out of scope: cross-entity relations

@dataclass
class QuantityPair:
    magnitude: Enum
    derivative: DerivativeDirection

@dataclass
class EntityState:
    entity: Entity
    state: Dict[str, QuantityPair]

@dataclass
class StateGraph:
    states: Dict[str, EntityState]
    edges: List[Tuple[str, str]]
