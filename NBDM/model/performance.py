# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Energy Performance Classes."""

from dataclasses import dataclass
from typing import Dict

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
    def from_dict(cls, _d: Dict) -> 'NBDM_SiteEnergy':
        obj = cls(
            consumption_gas = _d['consumption_gas'],
            consumption_electricity = _d['consumption_electricity'],
            consumption_district_heat = _d['consumption_district_heat'],
            consumption_other = _d['consumption_other'],
            production_solar_photovoltaic = _d['production_solar_photovoltaic'],
            production_solar_thermal = _d['production_solar_thermal'],
            production_other = _d['production_other'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


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
    def from_dict(cls, _d: Dict) -> 'NBDM_SourceEnergy':
        obj = cls(
            consumption_gas = _d['consumption_gas'],
            consumption_electricity = _d['consumption_electricity'],
            consumption_district_heat = _d['consumption_district_heat'],
            consumption_other = _d['consumption_other'],
            production_solar_photovoltaic = _d['production_solar_photovoltaic'],
            production_solar_thermal = _d['production_solar_thermal'],
            production_other = _d['production_other'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


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
    def from_dict(cls, _d: Dict) -> 'NBDM_AnnualHeatingDemandEnergy':
        obj = cls(
            annual_demand= _d['annual_demand'],
            losses_transmission= _d['losses_transmission'],
            losses_ventilation= _d['losses_ventilation'],
            gains_solar= _d['gains_solar'],
            gains_internal= _d['gains_internal'],
            utilization_factor= _d['utilization_factor'],
            gains_useful= _d['gains_useful'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


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
    def from_dict(cls, _d: Dict) -> 'NBDM_AnnualCoolingDemandEnergy':
        obj = cls(
            annual_demand = _d['annual_demand'],
            losses_transmission = _d['losses_transmission'],
            losses_ventilation = _d['losses_ventilation'],
            utilization_factor = _d['utilization_factor'],
            losses_useful = _d['losses_useful'],
            gains_solar = _d['gains_solar'],
            gains_internal = _d['gains_internal'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


@dataclass
class NBDM_PeakHeatingLoad:
    peak_load: float
    losses_transmission: float
    losses_ventilation: float
    gains_solar: float
    gains_internal: float
    utilization_factor: float
    gains_useful: float

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_PeakHeatingLoad':
        obj = cls(
            peak_load = _d['peak_load'],
            losses_transmission = _d['losses_transmission'],
            losses_ventilation = _d['losses_ventilation'],
            gains_solar = _d['gains_solar'],
            gains_internal = _d['gains_internal'],
            utilization_factor = _d['utilization_factor'],
            gains_useful = _d['gains_useful'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


@dataclass
class NBDM_PeakSensibleCoolingLoad:
    peak_load: float
    losses_transmission: float
    losses_ventilation: float
    utilization_factor: float
    losses_useful: float
    gains_solar: float
    gains_internal: float

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_PeakSensibleCoolingLoad':
        obj = cls(
            peak_load = _d['peak_load'],
            losses_transmission = _d['losses_transmission'],
            losses_ventilation = _d['losses_ventilation'],
            utilization_factor = _d['utilization_factor'],
            losses_useful = _d['losses_useful'],
            gains_solar = _d['gains_solar'],
            gains_internal = _d['gains_internal'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


@dataclass
class NBDM_BuildingSegmentPerformance:
    site_energy: NBDM_SiteEnergy
    source_energy: NBDM_SourceEnergy
    annual_heating_energy_demand: NBDM_AnnualHeatingDemandEnergy
    annual_cooling_energy_demand: NBDM_AnnualCoolingDemandEnergy
    peak_heating_load: NBDM_PeakHeatingLoad
    peak_sensible_cooling_load: NBDM_PeakSensibleCoolingLoad

    @classmethod
    def from_dict(cls, _d) -> 'NBDM_BuildingSegmentPerformance':
        obj = cls(
            site_energy = NBDM_SiteEnergy.from_dict(_d['site_energy']),
            source_energy = NBDM_SourceEnergy.from_dict(_d['source_energy']),
            annual_heating_energy_demand = NBDM_AnnualHeatingDemandEnergy.from_dict(_d['annual_heating_energy_demand']),
            annual_cooling_energy_demand = NBDM_AnnualCoolingDemandEnergy.from_dict(_d['annual_cooling_energy_demand']),
            peak_heating_load = NBDM_PeakHeatingLoad.from_dict(_d['peak_heating_load']),
            peak_sensible_cooling_load = NBDM_PeakSensibleCoolingLoad.from_dict(_d['peak_sensible_cooling_load']),
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj