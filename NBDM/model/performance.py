# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Energy Performance Classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from ph_units.unit_type import Unit

from NBDM.model import operations, serialization


@dataclass
class NBDM_SiteEnergy:
    consumption_gas: Unit = field(default_factory=Unit)
    consumption_electricity: Unit = field(default_factory=Unit)
    consumption_district_heat: Unit = field(default_factory=Unit)
    consumption_other: Unit = field(default_factory=Unit)
    production_solar_photovoltaic: Unit = field(default_factory=Unit)
    production_solar_thermal: Unit = field(default_factory=Unit)
    production_other: Unit = field(default_factory=Unit)

    @classmethod
    def from_dict(cls, _d: Dict[str, Unit]) -> NBDM_SiteEnergy:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __sub__(self, other: NBDM_SiteEnergy) -> NBDM_SiteEnergy:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_SiteEnergy) -> NBDM_SiteEnergy:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_SourceEnergy:
    consumption_gas: Unit = field(default_factory=Unit)
    consumption_electricity: Unit = field(default_factory=Unit)
    consumption_district_heat: Unit = field(default_factory=Unit)
    consumption_other: Unit = field(default_factory=Unit)
    production_solar_photovoltaic: Unit = field(default_factory=Unit)
    production_solar_thermal: Unit = field(default_factory=Unit)
    production_other: Unit = field(default_factory=Unit)

    @classmethod
    def from_dict(cls, _d: Dict[str, Unit]) -> NBDM_SourceEnergy:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __sub__(self, other: NBDM_SourceEnergy) -> NBDM_SourceEnergy:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_SourceEnergy) -> NBDM_SourceEnergy:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_AnnualHeatingDemandEnergy:
    heating_demand: Unit = field(default_factory=Unit)
    losses_transmission: Unit = field(default_factory=Unit)
    losses_ventilation: Unit = field(default_factory=Unit)
    gains_solar: Unit = field(default_factory=Unit)
    gains_internal: Unit = field(default_factory=Unit)
    utilization_factor: Unit = field(default_factory=Unit)

    @property
    def losses_total(self) -> Unit:
        return self.losses_transmission + self.losses_ventilation

    @property
    def gains_total(self) -> Unit:
        return (self.gains_internal + self.gains_solar) * self.utilization_factor

    @classmethod
    def from_dict(cls, _d: Dict[str, Unit]) -> NBDM_AnnualHeatingDemandEnergy:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    @classmethod
    def from_phpp_data(cls, _d: Dict[str, Unit]) -> NBDM_AnnualHeatingDemandEnergy:
        nbdm_obj = NBDM_AnnualHeatingDemandEnergy()
        for field_name in nbdm_obj.__dataclass_fields__.keys():
            nbdm_obj.__setattr__(field_name, _d[field_name])
        return nbdm_obj

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
    sensible_cooling_demand: Unit = field(default_factory=Unit)
    latent_cooling_demand: Unit = field(default_factory=Unit)
    losses_transmission: Unit = field(default_factory=Unit)
    losses_ventilation: Unit = field(default_factory=Unit)
    utilization_factor: Unit = field(default_factory=Unit)
    gains_solar: Unit = field(default_factory=Unit)
    gains_internal: Unit = field(default_factory=Unit)

    @property
    def total_cooling_demand(self) -> Unit:
        """Total cooling demand (sensible + latent)."""
        return self.sensible_cooling_demand + self.latent_cooling_demand

    @property
    def losses_total(self) -> Unit:
        return (
            self.losses_transmission + self.losses_ventilation
        ) * self.utilization_factor

    @property
    def gains_total(self) -> Unit:
        return self.gains_solar + self.gains_internal

    @classmethod
    def from_dict(cls, _d: Dict[str, Unit]) -> NBDM_AnnualCoolingDemandEnergy:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    @classmethod
    def from_phpp_data(cls, _d: Dict[str, Unit]) -> NBDM_AnnualCoolingDemandEnergy:
        nbdm_obj = NBDM_AnnualCoolingDemandEnergy()
        for field_name in nbdm_obj.__dataclass_fields__.keys():
            nbdm_obj.__setattr__(field_name, _d[field_name])
        return nbdm_obj

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
    peak_heating_load: Unit = field(default_factory=Unit)
    losses_transmission: Unit = field(default_factory=Unit)
    losses_ventilation: Unit = field(default_factory=Unit)
    gains_solar: Unit = field(default_factory=Unit)
    gains_internal: Unit = field(default_factory=Unit)

    @property
    def losses_total(self) -> Unit:
        return self.losses_transmission + self.losses_ventilation

    @property
    def gains_total(self) -> Unit:
        return self.gains_solar + self.gains_internal

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_PeakHeatingLoad:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    @classmethod
    def from_phpp_data(cls, _d: Dict[str, Unit]) -> NBDM_PeakHeatingLoad:
        nbdm_obj = NBDM_PeakHeatingLoad()
        for field_name in nbdm_obj.__dataclass_fields__.keys():
            nbdm_obj.__setattr__(field_name, _d[field_name])
        return nbdm_obj

    def __sub__(self, other: NBDM_PeakHeatingLoad) -> NBDM_PeakHeatingLoad:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_PeakHeatingLoad) -> NBDM_PeakHeatingLoad:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_PeakCoolingLoad:
    peak_sensible_cooling_load: Unit = field(default_factory=Unit)
    peak_latent_cooling_load: Unit = field(default_factory=Unit)
    losses_transmission: Unit = field(default_factory=Unit)
    losses_ventilation: Unit = field(default_factory=Unit)
    gains_solar: Unit = field(default_factory=Unit)
    gains_internal: Unit = field(default_factory=Unit)

    @property
    def losses_total(self) -> Unit:
        return self.losses_transmission + self.losses_ventilation

    @property
    def gains_total(self) -> Unit:
        return self.gains_solar + self.gains_internal

    @classmethod
    def from_dict(cls, _d: Dict[str, Unit]) -> NBDM_PeakCoolingLoad:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    @classmethod
    def from_phpp_data(cls, _d: Dict[str, Unit]) -> NBDM_PeakCoolingLoad:
        nbdm_obj = NBDM_PeakCoolingLoad()
        for field_name in nbdm_obj.__dataclass_fields__.keys():
            nbdm_obj.__setattr__(field_name, _d[field_name])
        return nbdm_obj

    def __sub__(self, other: NBDM_PeakCoolingLoad) -> NBDM_PeakCoolingLoad:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(self, other: NBDM_PeakCoolingLoad) -> NBDM_PeakCoolingLoad:
        return operations.add_NBDM_Objects(self, other)


@dataclass
class NBDM_BuildingSegmentPerformance:
    site_energy: NBDM_SiteEnergy = field(default_factory=NBDM_SiteEnergy)
    source_energy: NBDM_SourceEnergy = field(default_factory=NBDM_SourceEnergy)
    annual_heating_energy_demand: NBDM_AnnualHeatingDemandEnergy = field(
        default_factory=NBDM_AnnualHeatingDemandEnergy
    )
    annual_cooling_energy_demand: NBDM_AnnualCoolingDemandEnergy = field(
        default_factory=NBDM_AnnualCoolingDemandEnergy
    )

    peak_heating_load: NBDM_PeakHeatingLoad = field(default_factory=NBDM_PeakHeatingLoad)
    peak_cooling_load: NBDM_PeakCoolingLoad = field(default_factory=NBDM_PeakCoolingLoad)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentPerformance:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __sub__(
        self, other: NBDM_BuildingSegmentPerformance
    ) -> NBDM_BuildingSegmentPerformance:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentPerformance
    ) -> NBDM_BuildingSegmentPerformance:
        return operations.add_NBDM_Objects(self, other)
