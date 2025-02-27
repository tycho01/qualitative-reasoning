from qr import *
from container import *
from graph import *

container_state = {
  'inflow': (Inflow.ZERO, Direction.POSITIVE),
  'volume': (Volume.ZERO, Direction.NEUTRAL),
  'outflow': (Outflow.ZERO, Direction.NEUTRAL),
}

container_state_bonus = {
  **container_state,
  'height': (Height.ZERO, Direction.NEUTRAL),
  'pressure': (Pressure.ZERO, Direction.NEUTRAL),
}

entity_state = make_entity_state(container, container_state)
# entity_state = make_entity_state(bonus_container, container_state_bonus)
sg = gen_state_graph(entity_state)

print(f"states: {len(sg.states)}")
print(f"edges: {len(sg.edges)}")
draw_state_graph(sg)
