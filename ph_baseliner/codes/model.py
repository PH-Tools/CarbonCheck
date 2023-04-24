# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Data model of the Code."""

from pydantic import BaseModel, validator
from typing import Dict, Optional, Any, Self

from ph_units.converter import convert


# -----------------------------------------------------------------------------

class TableMaximumUFactor_Values(BaseModel):
    group_r: float
    all_other: float

    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field in v.__fields__:
            val = getattr(v, field)
            val = convert(val, kwargs["units"], "W/m2K")
            setattr(v, field, val)
        return v


class TableMaximumCFactor_Values(BaseModel):
    group_r: float
    all_other: float
    
    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field in v.__fields__:
            val = getattr(v, field)
            val = convert(val, kwargs["units"], "W/m2K")
            setattr(v, field, val)
        return v
    

class TableMaximumFFactor_Values(BaseModel):
    group_r: float
    all_other: float
    
    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field in v.__fields__:
            val = getattr(v, field)
            val = convert(val, kwargs["units"], "W/m2K")
            setattr(v, field, val)
        return v


class TableMaximumSHGC_Values(BaseModel):
    group_r: float
    all_other: float

    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        return v
    

# -----------------------------------------------------------------------------


class TableMaximumUFactor_ClimateZones(BaseModel):
    CZ4: TableMaximumUFactor_Values 
    CZ5: TableMaximumUFactor_Values
    CZ6: TableMaximumUFactor_Values

    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumCFactor_ClimateZones(BaseModel):
    CZ4: TableMaximumCFactor_Values 
    CZ5: TableMaximumCFactor_Values
    CZ6: TableMaximumCFactor_Values

    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumFFactor_ClimateZones(BaseModel):
    CZ4: TableMaximumFFactor_Values
    CZ5: TableMaximumFFactor_Values
    CZ6: TableMaximumFFactor_Values
    
    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumSHGC_ClimateZones(BaseModel):
    CZ4: TableMaximumSHGC_Values
    CZ5: TableMaximumSHGC_Values
    CZ6: TableMaximumSHGC_Values
    
    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        return v


# -----------------------------------------------------------------------------


class TableMaximumUFactorRoofs(BaseModel):
    insulation_above_deck: TableMaximumUFactor_ClimateZones
    metal_building: TableMaximumUFactor_ClimateZones
    attic_and_other: TableMaximumUFactor_ClimateZones

    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumUFactorWalls(BaseModel):
    mass: TableMaximumUFactor_ClimateZones
    metal_building: TableMaximumUFactor_ClimateZones
    metal_framed: TableMaximumUFactor_ClimateZones
    wood_framed_and_other: TableMaximumUFactor_ClimateZones
    below_grade: TableMaximumCFactor_ClimateZones

    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumUFactorFloors(BaseModel):
    mass: TableMaximumUFactor_ClimateZones
    joist_framed: TableMaximumUFactor_ClimateZones
    unheated_slab: TableMaximumFFactor_ClimateZones
    heated_slab: TableMaximumUFactor_ClimateZones

    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumUFactorFenestration(BaseModel):
    u_factors: TableMaximumUFactor_ClimateZones
    shgc: TableMaximumSHGC_ClimateZones
    
    @classmethod
    def convert_units(cls, v: Self, **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


# -----------------------------------------------------------------------------


class TableEnvelopeMaximumUFactors(BaseModel):
    name: str
    section: str
    units: str
    roofs: TableMaximumUFactorRoofs
    walls: TableMaximumUFactorWalls
    floors: TableMaximumUFactorFloors

    @validator("roofs", "walls", "floors", pre=False)
    @classmethod
    def convert_units(cls, v: Self, values: Dict):
        return type(v).convert_units(v, **values)


class TableFenestrationMaximumUFactors(BaseModel):  
    name: str
    section: str
    units: str
    fixed_windows: TableMaximumUFactorFenestration
    operable_windows: TableMaximumUFactorFenestration
    entrance_doors: TableMaximumUFactorFenestration
    skylights: TableMaximumUFactorFenestration
    
    @validator("fixed_windows", "operable_windows", "entrance_doors", "skylights", pre=False)
    @classmethod
    def convert_units(cls, v: Self, values: Dict):
        return type(v).convert_units(v, **values)


class TableLightingLPDAreaMethod(BaseModel):
    name: str
    section: str
    units: str
    LPD: dict
    
    @validator("LPD", pre=False)
    @classmethod
    def convert_units(cls, v: Dict, values: Dict):
        units = values["units"]
        for key, val in v.items():
            v[key] = convert(val, units, "W/m2")
        return v


# -----------------------------------------------------------------------------


class SectionMaximumFenestrationArea(BaseModel):
    source_url: str
    name: str
    section: str
    maximum_skylight_percent_of_roof: float
    maximum_window_percent_of_wall: float
    

# -----------------------------------------------------------------------------


class BaselineCodeTables(BaseModel):
    maximum_u_factors: TableEnvelopeMaximumUFactors
    fenestration_u_factors: TableFenestrationMaximumUFactors
    lighting_area_method: TableLightingLPDAreaMethod


class BaselineCodeSections(BaseModel):
    maximum_fenestration_area :SectionMaximumFenestrationArea


class BaselineCode(BaseModel):
    """Pydantic BaselineCode model."""
    name: str
    state: str
    year: str
    source_url: str
    tables: BaselineCodeTables
    sections: BaselineCodeSections
