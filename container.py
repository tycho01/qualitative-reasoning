'''causal model design: CONTAINERS'''

from qr import *

# quantities + spaces

# Inflow (of water into the container)

class Inflow(Enum):
  ZERO = 0  # POINT
  PLUS = 1  # RANGE

inflow =  Quantity('inflow', Inflow)

# Outflow (of water out of the container)

class Outflow(Enum):
  ZERO = 0  # POINT
  PLUS = 1  # RANGE
  MAX = 2   # POINT

outflow = Quantity('outflow', Outflow)

# Volume (of the water in the container)

class Volume(Enum):
  ZERO = 0  # POINT
  PLUS = 1  # RANGE
  MAX = 2   # POINT

volume =  Quantity('volume', Volume)

quantities = [
  inflow,
  outflow,
  volume,
]

# extra

# Height (of the water column in of container)

class Height(Enum):
  ZERO = 0  # POINT
  PLUS = 1  # RANGE
  MAX = 2   # POINT

height = Quantity('height', Height)

# Pressure (of the water column at the bottom of container)

class Pressure(Enum):
  ZERO = 0  # POINT
  PLUS = 1  # RANGE
  MAX = 2   # POINT

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
vol_out_max = ValueCorrespondence(('volume', Volume.MAX), ('outflow', Outflow.MAX))
# There is no outflow, when there is no ('volume', Volume.
vol_out_zero = ValueCorrespondence(('volume', Volume.ZERO), ('outflow', Outflow.ZERO))
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

vol_hi_max = ValueCorrespondence(('volume', Volume.MAX), ('height', Height.MAX))
vol_hi_zero = ValueCorrespondence(('volume', Volume.ZERO), ('height', Height.ZERO))
vol_prs_max = ValueCorrespondence(('volume', Volume.MAX), ('pressure', Pressure.MAX))
vol_prs_zero = ValueCorrespondence(('volume', Volume.ZERO), ('pressure', Pressure.ZERO))

hi_out_max = ValueCorrespondence(('height', Height.MAX), ('outflow', Outflow.MAX))
hi_out_zero = ValueCorrespondence(('height', Height.ZERO), ('outflow', Outflow.ZERO))
hi_vol_max = ValueCorrespondence(('height', Height.MAX), ('volume', Volume.MAX))
hi_vol_zero = ValueCorrespondence(('height', Height.ZERO), ('volume', Volume.ZERO))
hi_prs_max = ValueCorrespondence(('height', Height.MAX), ('pressure', Pressure.MAX))
hi_prs_zero = ValueCorrespondence(('height', Height.ZERO), ('pressure', Pressure.ZERO))

prs_out_max = ValueCorrespondence(('pressure', Pressure.MAX), ('outflow', Outflow.MAX))
prs_out_zero = ValueCorrespondence(('pressure', Pressure.ZERO), ('outflow', Outflow.ZERO))
prs_hi_max = ValueCorrespondence(('pressure', Pressure.MAX), ('height', Height.MAX))
prs_hi_zero = ValueCorrespondence(('pressure', Pressure.ZERO), ('height', Height.ZERO))
prs_vol_max = ValueCorrespondence(('pressure', Pressure.MAX), ('volume', Volume.MAX))
prs_vol_zero = ValueCorrespondence(('pressure', Pressure.ZERO), ('volume', Volume.ZERO))

out_vol_max = ValueCorrespondence(('outflow', Outflow.MAX), ('volume', Volume.MAX))
out_vol_zero = ValueCorrespondence(('outflow', Outflow.ZERO), ('volume', Volume.ZERO))
out_hi_max = ValueCorrespondence(('outflow', Outflow.MAX), ('height', Height.MAX))
out_hi_zero = ValueCorrespondence(('outflow', Outflow.ZERO), ('height', Height.ZERO))
out_prs_max = ValueCorrespondence(('outflow', Outflow.MAX), ('pressure', Pressure.MAX))
out_prs_zero = ValueCorrespondence(('outflow', Outflow.ZERO), ('pressure', Pressure.ZERO))

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

container = make_entity('container', quantities, relations)
# bonus_container = make_entity('container', all_quantities, all_relations)
