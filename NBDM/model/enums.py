# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Enum Classes."""

from __future__ import annotations
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


class appliance_type(Enum):
    DISHWASHER = 1
    CLOTHES_WASHER = 2
    CLOTHES_DRYER = 3
    REFRIGERATOR = 4
    FREEZER = 5
    FRIDGE_FREEZER = 6
    COOKING = 7
    CUSTOM = 11
    MEL = 13
    LIGHTING_INTERIOR = 14
    LIGHTING_EXTERIOR = 15
    LIGHTING_GARAGE = 16
    CUSTOM_LIGHTING = 17
    CUSTOM_MEL = 18
