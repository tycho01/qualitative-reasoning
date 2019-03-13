'''causal model design: CONTAINERS'''

from qr import *

# quantity spaces

class Volume(Enum):
  ZERO = 1
  PLUS = 2
  MAX = 3

class Outflow(Enum):
  ZERO = 1
  PLUS = 2
  MAX = 3

class Inflow(Enum):
  ZERO = 1
  PLUS = 2

# quantities

# Inflow (of water into the container)
inflow =  Quantity('inflow', Inflow)
# Outflow (of waterout of the container)
outflow = Quantity('outflow', Outflow)
# Volume (of the water in the container)
volume =  Quantity('volume', Volume)

quantities = [
  inflow,
  outflow,
  volume,
]

# relations

# The amount of inflow increases the volume
# inflow_volume  = Relationship(inflow,  volume, RelationType.INFLUENCE, Direction.POSITIVE)
inflow_volume  = Influence(inflow,  volume, Direction.POSITIVE)
# The amount of outflow decreases the volume
# outflow_volume = Relationship(outflow, volume, RelationType.INFLUENCE, Direction.NEGATIVE)
outflow_volume = Influence(outflow, volume, Direction.NEGATIVE)
# Outflow changes are proportional to volume changes
# volume_outflow = Relationship(volume, outflow, RelationType.PROPORTIONAL, Direction.POSITIVE)
volume_outflow = Proportional(volume, outflow, Direction.POSITIVE)
# The outflow is at its highest value (max), when the volume is at its highest value (also max).
vol_max = VC(Volume.MAX, Outflow.MAX)
# There is no outflow, when there is no volume.
vol_zero = VC(Volume.ZERO, Outflow.ZERO)
# Volume, Outflow, 

relations = [
  inflow_volume,
  outflow_volume,
  volume_outflow,
  vol_max,
  vol_zero,
]

# entities

container = Entity('container', quantities, relations)

# assumptions

# - How will the exogenously defined inflow behave? Choose assumptions at your discretion.

# state-graph with https://en.wikipedia.org/wiki/DOT_(graph_description_language)

# trace:
# - intra-state
# - inter-state
