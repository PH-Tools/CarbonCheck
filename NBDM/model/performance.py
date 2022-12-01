# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Energy Performance Classes."""

from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization


@dataclass
class NBDM_SiteEnergy:
    consumption_gas: float
    consumption_electricity: float
    consumption_district_heat: float
    consumption_other: float
    production_solar_photovoltaic: float
    production_solar_thermal: float
    production_other: float

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_SiteEnergy":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_SourceEnergy:
    consumption_gas: float
    consumption_electricity: float
    consumption_district_heat: float
    consumption_other: float
    production_solar_photovoltaic: float
    production_solar_thermal: float
    production_other: float

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_SourceEnergy":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_AnnualHeatingDemandEnergy:
    annual_demand: float
    losses_transmission: float
    losses_ventilation: float
    gains_solar: float
    gains_internal: float
    utilization_factor: float
    gains_useful: float

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_AnnualHeatingDemandEnergy":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_AnnualCoolingDemandEnergy:
    annual_demand: float
    losses_transmission: float
    losses_ventilation: float
    utilization_factor: float
    losses_useful: float
    gains_solar: float
    gains_internal: float

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_AnnualCoolingDemandEnergy":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_PeakHeatingLoad:
    peak_load: float
    losses_transmission: float
    losses_ventilation: float
    gains_solar: float
    gains_internal: float

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_PeakHeatingLoad":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_PeakSensibleCoolingLoad:
    peak_load: float
    losses_transmission: float
    losses_ventilation: float
    gains_solar: float
    gains_internal: float

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_PeakSensibleCoolingLoad":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_BuildingSegmentPerformance:
    site_energy: NBDM_SiteEnergy
    source_energy: NBDM_SourceEnergy
    annual_heating_energy_demand: NBDM_AnnualHeatingDemandEnergy
    annual_cooling_energy_demand: NBDM_AnnualCoolingDemandEnergy
    peak_heating_load: NBDM_PeakHeatingLoad
    peak_sensible_cooling_load: NBDM_PeakSensibleCoolingLoad

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_BuildingSegmentPerformance":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)
