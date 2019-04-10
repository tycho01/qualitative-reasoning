'''causal model design: CONTAINERS'''

from qr import *

# quantities + spaces

# Inflow (of water into the container)

class Inflow(Enum):
    ZERO = 0
    PLUS = 1

inflow =  Quantity('inflow', Inflow)

# Outflow (of water out of the container)

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
inflow_volume  = Influence(inflow,  volume, Direction.POSITIVE)
# The amount of outflow decreases the volume
outflow_volume = Influence(outflow, volume, Direction.NEGATIVE)
# Outflow changes are proportional to volume changes
volume_outflow = Proportional(volume, outflow, Direction.POSITIVE)
# The outflow is at its highest value (max), when the volume is at its highest value (also max).
vol_out_max = ValueCorrespondence(('volume', Volume.MAX), ('outflow', Outflow.MAX))
# There is no outflow, when there is no volume.
vol_out_zero = ValueCorrespondence(('volume', Volume.ZERO), ('outflow', Outflow.ZERO))

relations = [
    inflow_volume,
    outflow_volume,
    volume_outflow,
    vol_out_max,
    vol_out_zero,
]

# extra relations

# Height changes are proportional to volume changes
volume_height =   Proportional(volume, height,   Direction.POSITIVE)
# Pressure changes are proportional to height changes
height_pressure = Proportional(height, pressure, Direction.POSITIVE)
# Instead of volume, it is the pressure that determines the outflow
pressure_outflow = Proportional(pressure, outflow, Direction.POSITIVE)
# Particular values, such as 0 and max correspond for volume, height, pressure and outflow.

vol_hi_max = ValueCorrespondence(('volume', Volume.MAX), ('height', Height.MAX))
vol_hi_zero = ValueCorrespondence(('volume', Volume.ZERO), ('height', Height.ZERO))
hi_prs_max = ValueCorrespondence(('height', Height.MAX), ('pressure', Pressure.MAX))
hi_prs_zero = ValueCorrespondence(('height', Height.ZERO), ('pressure', Pressure.ZERO))
prs_out_max = ValueCorrespondence(('pressure', Pressure.MAX), ('outflow', Outflow.MAX))
prs_out_zero = ValueCorrespondence(('pressure', Pressure.ZERO), ('outflow', Outflow.ZERO))

all_relations = [
    inflow_volume,
    outflow_volume,
    # volume_outflow,  # Instead of volume, it is the pressure that determines the outflow

    # Particular values, such as 0 and max correspond for volume, height, pressure and outflow.
    vol_hi_max,
    vol_hi_zero,
    hi_prs_max,
    hi_prs_zero,
    prs_out_max,
    prs_out_zero,

    # extra relations
    volume_height,
    height_pressure,
    pressure_outflow,
]

# entities

container = make_entity('container', quantities, relations)
bonus_container = make_entity('container', all_quantities, all_relations)
