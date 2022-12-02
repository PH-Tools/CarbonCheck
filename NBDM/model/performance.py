# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Energy Performance Classes."""

from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization
from NBDM.model import operations


@dataclass
class NBDM_EnergyCost:
    cost_gas: float
    cost_electricity: float
    cost_district_heat: float
    cost_other_energy: float

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_EnergyCost":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(self, other: "NBDM_EnergyCost") -> "NBDM_EnergyCost":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: "NBDM_EnergyCost") -> "NBDM_EnergyCost":
        return operations.add_NBDM_Objects(self, other)


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

    def __sub__(self, other: "NBDM_SiteEnergy") -> "NBDM_SiteEnergy":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: "NBDM_SiteEnergy") -> "NBDM_SiteEnergy":
        return operations.add_NBDM_Objects(self, other)


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

    def __sub__(self, other: "NBDM_SourceEnergy") -> "NBDM_SourceEnergy":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: "NBDM_SourceEnergy") -> "NBDM_SourceEnergy":
        return operations.add_NBDM_Objects(self, other)


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

    def __sub__(
        self, other: "NBDM_AnnualHeatingDemandEnergy"
    ) -> "NBDM_AnnualHeatingDemandEnergy":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: "NBDM_AnnualHeatingDemandEnergy"
    ) -> "NBDM_AnnualHeatingDemandEnergy":
        return operations.add_NBDM_Objects(self, other)


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

    def __sub__(
        self, other: "NBDM_AnnualCoolingDemandEnergy"
    ) -> "NBDM_AnnualCoolingDemandEnergy":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: "NBDM_AnnualCoolingDemandEnergy"
    ) -> "NBDM_AnnualCoolingDemandEnergy":
        return operations.add_NBDM_Objects(self, other)


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

    def __sub__(self, other: "NBDM_PeakHeatingLoad") -> "NBDM_PeakHeatingLoad":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: "NBDM_PeakHeatingLoad") -> "NBDM_PeakHeatingLoad":
        return operations.add_NBDM_Objects(self, other)


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

    def __sub__(
        self, other: "NBDM_PeakSensibleCoolingLoad"
    ) -> "NBDM_PeakSensibleCoolingLoad":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: "NBDM_PeakSensibleCoolingLoad"
    ) -> "NBDM_PeakSensibleCoolingLoad":
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_BuildingSegmentPerformance:
    site_energy: NBDM_SiteEnergy
    source_energy: NBDM_SourceEnergy
    energy_cost: NBDM_EnergyCost
    annual_heating_energy_demand: NBDM_AnnualHeatingDemandEnergy
    annual_cooling_energy_demand: NBDM_AnnualCoolingDemandEnergy
    peak_heating_load: NBDM_PeakHeatingLoad
    peak_sensible_cooling_load: NBDM_PeakSensibleCoolingLoad

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_BuildingSegmentPerformance":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(
        self, other: "NBDM_BuildingSegmentPerformance"
    ) -> "NBDM_BuildingSegmentPerformance":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: "NBDM_BuildingSegmentPerformance"
    ) -> "NBDM_BuildingSegmentPerformance":
        return operations.add_NBDM_Objects(self, other)
