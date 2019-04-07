from qr_types import *
from qr import *
from container import *

# initialize state as per example slide

container_state = {
    'volume': (Volume.ZERO, Direction.NEUTRAL),
    'inflow': (Inflow.ZERO, Direction.POSITIVE),
    'outflow': (Outflow.ZERO, Direction.NEUTRAL),
}

bonus_container_state = {
    **container_state,
    'height': (Height.ZERO, Direction.NEUTRAL),
    'pressure': (Volume.ZERO, Direction.NEUTRAL),
}

entity_state = make_entity_state(container, container_state)
bonus_entity_state = make_entity_state(bonus_container, bonus_container_state)
