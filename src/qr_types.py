from enum import Enum, EnumMeta
from dataclasses import dataclass
from typing import List, Dict, Tuple
from frozen import FrozenDict

import re
import yaml

# values for Direction don't follow semantic conventions of quantity spaces (see below)
# only the ordinal property is used, outside of QUESTION.
class Direction(Enum):
    QUESTION = 0  # question mark option to indicate changes in both directions causing an ambiguous change
    NEGATIVE = 1
    NEUTRAL  = 2
    POSITIVE = 3

# for each quantity space we need to know:
# - the order (in which to transition), so ensure the enums are logically ordered!
# - what is negative or positive (needed for influence relation?) - ensure underlying values reflect this!
# - represent point values as even numbers (-> makes 0 a point), ranges as odd numbers.
@dataclass(frozen=True)
class Quantity:
    name: str
    quantitySpace: EnumMeta

@dataclass(frozen=True)
class Relation:
    # a: any
    # b: any
    pass

@dataclass(frozen=True)
class Relationship(Relation):
    a: Quantity
    b: Quantity
    # ^ EnumMeta?

@dataclass(frozen=True)
class Influence(Relationship):
     correlation: Direction = Direction.POSITIVE

@dataclass(frozen=True)
class Proportional(Relationship):
    correlation: Direction = Direction.POSITIVE

@dataclass(frozen=True)
class ValueCorrespondence(Relation):
    '''if a then b. a/b denote (quantity name, enum value)'''
    a: Tuple[str, Enum]
    b: Tuple[str, Enum]

@dataclass(frozen=True)
class Entity:
    name: str
    quantities: Dict[str, Quantity]
    relations: List[Relation]
    # ^ out of scope: cross-entity relations

@dataclass(frozen=True)
class QuantityPair:
    magnitude: Enum
    derivative: Direction

@dataclass(frozen=True)
class EntityState:
    entity: Entity
    state: Dict[str, QuantityPair]

    def __hash__(self) -> int:
        return hash(state_key(self))

def state_key(state: EntityState) -> str:
    '''serialize state for graph key purposes'''
    return re.sub(r"[^\w]+", '_', serialize_state(state))

def serialize_state(state: EntityState) -> str:
    '''simple serialization method for EntityState'''
    return yaml.dump({k: f"({pair.magnitude.value}, {pair.derivative.value})" for k, pair in state.state.items()})

@dataclass(frozen=True)
class StateGraph:
    states: Dict[str, EntityState]
    edges: List[Tuple[str, str]]
