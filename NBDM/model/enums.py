from enum import Enum, auto


class building_type(Enum):
    MULTIFAMILY = "Multi-Family"
    NONRESIDENTIAL = "Non-Residential"


class construction_type(Enum):
    NEW_CONSTRUCTION = auto()
    ADAPTIVE_REUSE = auto()
    GUT_REHAB = auto()
