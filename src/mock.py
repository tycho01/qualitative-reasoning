from qr_types import *
from qr import *
from container import *

# initialize state as per example slide

container_state = {
    'volume': (Volume.ZERO, DerivativeDirection.NEUTRAL),
    'inflow': (Inflow.ZERO, DerivativeDirection.NEUTRAL),
    'outflow': (Outflow.ZERO, DerivativeDirection.NEUTRAL),
}

bonus_container_state = {
    **container_state,
    'height': (Height.ZERO, DerivativeDirection.NEUTRAL),
    'pressure': (Volume.ZERO, DerivativeDirection.NEUTRAL),
}

entity_state = make_entity_state(container, container_state)
bonus_entity_state = make_entity_state(bonus_container, bonus_container_state)
