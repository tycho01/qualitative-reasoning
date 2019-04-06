from qr import *
from container import *

# initialize state as per example slide

container_state = {
    'volume': (Volume.ZERO, Direction.NEUTRAL),
    'inflow': (Inflow.ZERO, Direction.NEUTRAL),
    'outflow': (Outflow.ZERO, Direction.NEUTRAL),
}

container_state_bonus = {
    **container_state,
    'height': (Height.ZERO, Direction.NEUTRAL),
    'pressure': (Volume.ZERO, Direction.NEUTRAL),
}

entity_state = EntityState(container, container_state)
