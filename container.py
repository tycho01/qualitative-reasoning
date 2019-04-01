'''causal model design: CONTAINERS'''

from qr import *

# quantities + spaces

# Inflow (of water into the container)

class Inflow(Enum):
  ZERO = 0
  PLUS = 1

inflow =  Quantity('inflow', Inflow)

# Outflow (of waterout of the container)

class Outflow(Enum):
  ZERO = 0
  PLUS = 1
  MAX = 2

outflow = Quantity('outflow', Outflow)

# Volume (of the water in the container)

class Volume(Enum):
  ZERO = 0
  PLUS = 1
  MAX = 2

volume =  Quantity('volume', Volume)

quantities = [
  inflow,
  outflow,
  volume,
]

# extra

# Height (of the water column in of container)

class Height(Enum):
  ZERO = 0
  PLUS = 1
  MAX = 2

height = Quantity('height', Height)

# Pressure (of the water column at the bottom of container)

class Pressure(Enum):
  ZERO = 0
  PLUS = 1
  MAX = 2

pressure = Quantity('pressure', Pressure)

all_quantities = [*quantities, height, pressure]

# relations

# The amount of inflow increases the volume
# inflow_volume  = Relationship(inflow,  volume, RelationType.INFLUENCE, RelationDirection.POSITIVE)
inflow_volume  = Influence(inflow,  volume, RelationDirection.POSITIVE)
# The amount of outflow decreases the volume
# outflow_volume = Relationship(outflow, volume, RelationType.INFLUENCE, RelationDirection.NEGATIVE)
outflow_volume = Influence(outflow, volume, RelationDirection.NEGATIVE)
# Outflow changes are proportional to volume changes
# volume_outflow = Relationship(volume, outflow, RelationType.PROPORTIONAL, RelationDirection.POSITIVE)
volume_outflow = Proportional(volume, outflow, RelationDirection.POSITIVE)
# The outflow is at its highest value (max), when the volume is at its highest value (also max).
vol_out_max = ValueCorrespondence(Volume.MAX, Outflow.MAX)
# There is no outflow, when there is no volume.
vol_out_zero = ValueCorrespondence(Volume.ZERO, Outflow.ZERO)
# Volume, Outflow, 

relations = [
  inflow_volume,
  outflow_volume,
  volume_outflow,
  vol_out_max,
  vol_out_zero,
]

# extra relations

# Height changes are proportional to volume changes
volume_height =   Proportional(volume, height,   RelationDirection.POSITIVE)
# Pressure changes are proportional to height changes
height_pressure = Proportional(height, pressure, RelationDirection.POSITIVE)
# Instead of volume, it is the pressure that determines the outflow
pressure_outflow = Proportional(pressure, outflow, RelationDirection.POSITIVE)
# Particular values, such as 0 and max correspond for volume, height, pressure and outflow.

vol_hi_max = ValueCorrespondence(Volume.MAX, Height.MAX)
vol_hi_zero = ValueCorrespondence(Volume.ZERO, Height.ZERO)
vol_prs_max = ValueCorrespondence(Volume.MAX, Pressure.MAX)
vol_prs_zero = ValueCorrespondence(Volume.ZERO, Pressure.ZERO)

hi_out_max = ValueCorrespondence(Height.MAX, Outflow.MAX)
hi_out_zero = ValueCorrespondence(Height.ZERO, Outflow.ZERO)
hi_vol_max = ValueCorrespondence(Height.MAX, Volume.MAX)
hi_vol_zero = ValueCorrespondence(Height.ZERO, Volume.ZERO)
hi_prs_max = ValueCorrespondence(Height.MAX, Pressure.MAX)
hi_prs_zero = ValueCorrespondence(Height.ZERO, Pressure.ZERO)

prs_out_max = ValueCorrespondence(Pressure.MAX, Outflow.MAX)
prs_out_zero = ValueCorrespondence(Pressure.ZERO, Outflow.ZERO)
prs_hi_max = ValueCorrespondence(Pressure.MAX, Height.MAX)
prs_hi_zero = ValueCorrespondence(Pressure.ZERO, Height.ZERO)
prs_vol_max = ValueCorrespondence(Pressure.MAX, Volume.MAX)
prs_vol_zero = ValueCorrespondence(Pressure.ZERO, Volume.ZERO)

out_vol_max = ValueCorrespondence(Outflow.MAX, Volume.MAX)
out_vol_zero = ValueCorrespondence(Outflow.ZERO, Volume.ZERO)
out_hi_max = ValueCorrespondence(Outflow.MAX, Height.MAX)
out_hi_zero = ValueCorrespondence(Outflow.ZERO, Height.ZERO)
out_prs_max = ValueCorrespondence(Outflow.MAX, Pressure.MAX)
out_prs_zero = ValueCorrespondence(Outflow.ZERO, Pressure.ZERO)

all_relations = [
  inflow_volume,
  outflow_volume,
  # volume_outflow,  # Instead of volume, it is the pressure that determines the outflow

  # TODO: figure out which of these are legit

  # Particular values, such as 0 and max correspond for volume, height, pressure and outflow.
  vol_out_max,
  vol_out_zero,
  vol_hi_max,
  vol_hi_zero,
  vol_prs_max,
  vol_prs_zero,

  hi_out_max,
  hi_out_zero,
  hi_vol_max,
  hi_vol_zero,
  hi_prs_max,
  hi_prs_zero,

  prs_out_max,
  prs_out_zero,
  prs_hi_max,
  prs_hi_zero,
  prs_vol_max,
  prs_vol_zero,

  out_vol_max,
  out_vol_zero,
  out_hi_max,
  out_hi_zero,
  out_prs_max,
  out_prs_zero,

  # extra relations

  volume_height,
  height_pressure,
  pressure_outflow,
]

# entities

container = Entity('container', quantities, relations)
# extra_container = Entity('container', all_quantities, all_relations)


