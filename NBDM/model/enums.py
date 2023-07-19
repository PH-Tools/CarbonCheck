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
    DISHWASHER = "Dishwasher"
    CLOTHES_WASHER = "Clothes Washer"
    CLOTHES_DRYER = "Clothes Dryer"
    REFRIGERATOR = "Refrigerator"
    FREEZER = "Freezer"
    FRIDGE_FREEZER = "Fridge / Freezer"
    COOKING = "Cooking"
    CUSTOM = "Custom"
    MEL = "Misc. Electric Loads"
    LIGHTING_INTERIOR = "Interior Lighting"
    LIGHTING_EXTERIOR = "Exterior Lighting"
    LIGHTING_GARAGE = "Garage Lighting"
    CUSTOM_LIGHTING = "Custom Lighting"
    CUSTOM_MEL = "Custom MEL"


class heating_device_type(Enum):
    NONE = "None"
    COMPACT_HEAT_PUMP = "Compact Heat Pumps"
    HEAT_PUMP = "Heat Pumps"
    DISTRICT_HEATING = "District Heating"
    BOILER = "Boilers"
    DIRECT_ELECTRIC = "Direct Electric"
    OTHER = "Other"


class cooling_device_type(Enum):
    NONE = "None"
    SUPPLY_AIR = "Ventilation Supply Air"
    RECIRCULATION_AIR = "Recirculation Air"
    DEHUMIDIFICATION = "Dedicated Dehumidification"
    PANEL = "Panel Cooling"

class dhw_tank_device_type(Enum):
    NONE = "None"
