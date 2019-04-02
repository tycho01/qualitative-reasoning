# from graph import *
from qr import *
from container import *

# initialize state as per example slide

container_state = {
  'volume': (Volume.ZERO, Direction.NEUTRAL),
  'inflow': (Inflow.ZERO, Direction.NEUTRAL),
  'outflow': (Outflow.ZERO, Direction.NEUTRAL),
}

entity_state = EntityState(container, container_state)
state = State({ 'container': entity_state })
# state = State(entity_state)
print(state)
# gen_states(state)
sg = gen_state_graph(state)
draw_state_graph(sg)
