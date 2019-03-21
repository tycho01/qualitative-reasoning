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
# sg = gen_state_graph(state)
# draw_state_graph(sg)
print(state)
gen_states(state)

# assumptions
# - continuous: will go through intermediate ordinal states

# - How will the exogenously defined inflow behave? Choose assumptions at your discretion.

# state-graph with https://en.wikipedia.org/wiki/DOT_(graph_description_language)

# trace:
# - intra-state
# - inter-state

# we list the assumptions on e.g. user inputs / starting states,
# which in turn decide what will happen in the simulation

# interpretations:
# - go from initial state
# - generate all possible states and see how they connect
# - generate states, see which lead to conflicts based on rules like VC,
#   then generate edges using Influence/Proportional relationships (does this imply an initial state?)
# - user interaction
