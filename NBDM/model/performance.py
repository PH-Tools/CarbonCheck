# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Energy Performance Classes."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization
from NBDM.model import operations


@dataclass
class NBDM_EnergyCost:
    cost_gas: float = 0.0
    cost_electricity: float = 0.0
    cost_district_heat: float = 0.0
    cost_other_energy: float = 0.0

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_EnergyCost:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(self, other: NBDM_EnergyCost) -> NBDM_EnergyCost:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_EnergyCost) -> NBDM_EnergyCost:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_SiteEnergy:
    consumption_gas: float = 0.0
    consumption_electricity: float = 0.0
    consumption_district_heat: float = 0.0
    consumption_other: float = 0.0
    production_solar_photovoltaic: float = 0.0
    production_solar_thermal: float = 0.0
    production_other: float = 0.0

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_SiteEnergy:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(self, other: NBDM_SiteEnergy) -> NBDM_SiteEnergy:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_SiteEnergy) -> NBDM_SiteEnergy:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_SourceEnergy:
    consumption_gas: float = 0.0
    consumption_electricity: float = 0.0
    consumption_district_heat: float = 0.0
    consumption_other: float = 0.0
    production_solar_photovoltaic: float = 0.0
    production_solar_thermal: float = 0.0
    production_other: float = 0.0

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_SourceEnergy:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(self, other: NBDM_SourceEnergy) -> NBDM_SourceEnergy:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_SourceEnergy) -> NBDM_SourceEnergy:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_AnnualHeatingDemandEnergy:
    heating_demand: float = 0.0
    losses_transmission: float = 0.0
    losses_ventilation: float = 0.0
    gains_solar: float = 0.0
    gains_internal: float = 0.0
    utilization_factor: float = 0.0

    @property
    def losses_total(self) -> float:
        return self.losses_transmission + self.losses_ventilation

    @property
    def gains_total(self) -> float:
        return (self.gains_internal + self.gains_solar) * self.utilization_factor

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_AnnualHeatingDemandEnergy:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(
        self, other: NBDM_AnnualHeatingDemandEnergy
    ) -> NBDM_AnnualHeatingDemandEnergy:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_AnnualHeatingDemandEnergy
    ) -> NBDM_AnnualHeatingDemandEnergy:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_AnnualCoolingDemandEnergy:
    sensible_cooling_demand: float = 0.0
    latent_cooling_demand: float = 0.0
    losses_transmission: float = 0.0
    losses_ventilation: float = 0.0
    utilization_factor: float = 0.0
    gains_solar: float = 0.0
    gains_internal: float = 0.0

    @property
    def losses_total(self) -> float:
        return (
            self.losses_transmission + self.losses_ventilation
        ) * self.utilization_factor

    @property
    def gains_total(self) -> float:
        return self.gains_solar + self.gains_internal

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_AnnualCoolingDemandEnergy:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(
        self, other: NBDM_AnnualCoolingDemandEnergy
    ) -> NBDM_AnnualCoolingDemandEnergy:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_AnnualCoolingDemandEnergy
    ) -> NBDM_AnnualCoolingDemandEnergy:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_PeakHeatingLoad:
    peak_load: float = 0.0
    losses_transmission: float = 0.0
    losses_ventilation: float = 0.0
    gains_solar: float = 0.0
    gains_internal: float = 0.0

    @property
    def losses_total(self) -> float:
        return self.losses_transmission + self.losses_ventilation

    @property
    def gains_total(self) -> float:
        return self.gains_solar + self.gains_internal

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_PeakHeatingLoad:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(self, other: NBDM_PeakHeatingLoad) -> NBDM_PeakHeatingLoad:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_PeakHeatingLoad) -> NBDM_PeakHeatingLoad:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_PeakCoolingLoad:
    peak_load_sensible: float = 0.0
    peak_load_latent: float = 0.0
    losses_transmission: float = 0.0
    losses_ventilation: float = 0.0
    gains_solar: float = 0.0
    gains_internal: float = 0.0

    @property
    def losses_total(self) -> float:
        return self.losses_transmission + self.losses_ventilation

    @property
    def gains_total(self) -> float:
        return self.gains_solar + self.gains_internal

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_PeakCoolingLoad:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(self, other: NBDM_PeakCoolingLoad) -> NBDM_PeakCoolingLoad:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_PeakCoolingLoad) -> NBDM_PeakCoolingLoad:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_BuildingSegmentPerformance:
    site_energy: NBDM_SiteEnergy = NBDM_SiteEnergy()
    source_energy: NBDM_SourceEnergy = NBDM_SourceEnergy()
    energy_cost: NBDM_EnergyCost = NBDM_EnergyCost()
    annual_heating_energy_demand: NBDM_AnnualHeatingDemandEnergy = (
        NBDM_AnnualHeatingDemandEnergy()
    )
    annual_cooling_energy_demand: NBDM_AnnualCoolingDemandEnergy = (
        NBDM_AnnualCoolingDemandEnergy()
    )
    peak_heating_load: NBDM_PeakHeatingLoad = NBDM_PeakHeatingLoad()
    peak_sensible_cooling_load: NBDM_PeakCoolingLoad = NBDM_PeakCoolingLoad()

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentPerformance:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(
        self, other: NBDM_BuildingSegmentPerformance
    ) -> NBDM_BuildingSegmentPerformance:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentPerformance
    ) -> NBDM_BuildingSegmentPerformance:
        return operations.add_NBDM_Objects(self, other)
