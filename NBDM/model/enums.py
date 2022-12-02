from enum import Enum


class building_type(Enum):
    MULTIFAMILY = "Multi-Family"
    NONRESIDENTIAL = "Non-Residential"


class construction_type(Enum):
    NEW_CONSTRUCTION = "New Construction"
    ADAPTIVE_REUSE = "Adaptive Reuse"
    GUT_REHAB = "Gut Rehab"


class construction_method(Enum):
    METHOD_A = "Method A"
    METHOD_B = "Method B"


class nyc_ecc_year(Enum):
    _2019 = "2019"
    _2023 = "2023"
