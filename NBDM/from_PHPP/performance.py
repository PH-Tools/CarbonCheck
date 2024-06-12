# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Performance objects from PHPP data."""

from collections import defaultdict
from enum import Enum
from functools import reduce
from typing import Dict, List, Optional, Tuple

from ph_units.unit_type import Unit
from PHX.PHPP import phpp_app

from NBDM.model import performance

# -----------------------------------------------------------------------------


class EnergyType(Enum):
    ELECTRICITY = "ELECTRICITY"
    NATURAL_GAS = "GAS"
    OIL = "OIL"
    DISTRICT_HEAT = "DISTRICT"
    PV_ELECTRICITY = "PV ELECTRICITY"
    SOLAR_THERMAL = "SOLAR THERMAL"
    OTHER = "OTHER"


CONSUMPTION_USES = ["HEATING", "COOLING", "DHW", "HOUSEHOLD_ELECTRIC", "ADDITIONAL_GAS"]
GENERATION_USES = ["ENERGY_GENERATION"]

# -----------------------------------------------------------------------------
# -- Site Energy


def get_consumption_uses(_data: Dict[str, Dict[str, Unit]]) -> dict[str, Dict[str, Unit]]:
    """Return the Energy Consumption use-types (heating, cooling etc..)"""
    return {k: v for k, v in _data.items() if k.upper().strip() in CONSUMPTION_USES}


def get_production_uses(_data: Dict[str, Dict[str, Unit]]) -> dict[str, Dict[str, Unit]]:
    """Return the Energy Production use types (Energy Generation)"""
    return {k: v for k, v in _data.items() if k.upper().strip() not in CONSUMPTION_USES}


def organize_energy_by_fuel_type(
    _data: Dict[str, Dict[str, Unit]]
) -> Dict[str, List[Tuple[str, Unit]]]:
    """Reorganize the data so energy use is grouped by fuel-type.
    ie: -> {
            "ELECTRICITY": [(k,v), (k,v)...],
            "NATURAL_GAS": [(k,v), (k,v)...] ,
            ...
            }"
    """

    d: Dict[str, List[Tuple[str, Unit]]] = defaultdict(list)
    for use_type_name, energy_usage_dict in _data.items():
        for k, v in energy_usage_dict.items():
            # -- Note: 'PV-Electricity' has to come before 'Electricity' for it to work.
            # -- otherwise it gets logged as regular 'Electricity'
            # -- must be a better way then using 'in' ?
            if v is None:
                continue
            elif EnergyType.PV_ELECTRICITY.value in str(k).upper().strip():
                d[EnergyType.PV_ELECTRICITY.value].append((f"{use_type_name} - {k}", v))
            elif EnergyType.SOLAR_THERMAL.value in str(k).upper().strip():
                d[EnergyType.SOLAR_THERMAL.value].append((f"{use_type_name} - {k}", v))
            elif EnergyType.ELECTRICITY.value in str(k).upper().strip():
                d[EnergyType.ELECTRICITY.value].append((f"{use_type_name} - {k}", v))
            elif EnergyType.NATURAL_GAS.value in str(k).upper().strip():
                d[EnergyType.NATURAL_GAS.value].append((f"{use_type_name} - {k}", v))
            elif EnergyType.DISTRICT_HEAT.value in str(k).upper().strip():
                d[EnergyType.DISTRICT_HEAT.value].append((f"{use_type_name} - {k}", v))
            else:
                d[EnergyType.OTHER.value].append((f"OTHER - {k}", v))
    return d


def sum_energy_values(_data: Dict[str, List[Tuple[str, Unit]]], _key: str) -> Unit:
    """Return a single total value for energy consumption/production by the specified type."""
    data_list: List[Unit] = [tpl[1] for tpl in _data.get(_key, [])]
    if not data_list:
        return Unit(0.0, "-")

    return reduce(lambda x, y: x + y, data_list)


def build_site_energy(_data: Dict[str, Dict[str, Unit]]) -> performance.NBDM_SiteEnergy:
    # -- Energy Use Data
    consumption = organize_energy_by_fuel_type(get_consumption_uses(_data))
    production = organize_energy_by_fuel_type(get_production_uses(_data))

    return performance.NBDM_SiteEnergy(
        sum_energy_values(consumption, EnergyType.NATURAL_GAS.value),
        sum_energy_values(consumption, EnergyType.ELECTRICITY.value),
        sum_energy_values(consumption, EnergyType.DISTRICT_HEAT.value),
        sum_energy_values(consumption, EnergyType.OTHER.value),
        sum_energy_values(production, EnergyType.PV_ELECTRICITY.value),
        sum_energy_values(production, EnergyType.SOLAR_THERMAL.value),
        sum_energy_values(production, EnergyType.OTHER.value),
    )


def build_source_energy(
    _data: Dict[str, Dict[str, Unit]]
) -> performance.NBDM_SourceEnergy:
    # -- Energy Use Data
    consumption = organize_energy_by_fuel_type(get_consumption_uses(_data))
    production = organize_energy_by_fuel_type(get_production_uses(_data))

    return performance.NBDM_SourceEnergy(
        sum_energy_values(consumption, EnergyType.NATURAL_GAS.value),
        sum_energy_values(consumption, EnergyType.ELECTRICITY.value),
        sum_energy_values(consumption, EnergyType.DISTRICT_HEAT.value),
        sum_energy_values(consumption, EnergyType.OTHER.value),
        sum_energy_values(production, EnergyType.PV_ELECTRICITY.value),
        sum_energy_values(production, EnergyType.SOLAR_THERMAL.value),
        sum_energy_values(production, EnergyType.OTHER.value),
    )


# -----------------------------------------------------------------------------
# -- Annual Energy Demand


def build_annual_heating_demand(
    _data: Dict[str, Unit],
) -> performance.NBDM_AnnualHeatingDemandEnergy:
    return performance.NBDM_AnnualHeatingDemandEnergy.from_phpp_data(_data)


def build_annual_cooling_demand(
    _data: Dict[str, Unit],
) -> performance.NBDM_AnnualCoolingDemandEnergy:
    return performance.NBDM_AnnualCoolingDemandEnergy.from_phpp_data(_data)


# -----------------------------------------------------------------------------
# -- Peak Loads


def largest_peak_heating_load(
    _phpp_data_load_1: Dict[str, Unit], _phpp_data_load_2: Dict[str, Unit]
) -> Dict[str, Unit]:
    """Return the largest peak heating load data-set."""

    peak_load_1 = _phpp_data_load_1["peak_heating_load"]
    peak_load_2 = _phpp_data_load_2["peak_heating_load"]

    if peak_load_1 > peak_load_2:
        return _phpp_data_load_1
    else:
        return _phpp_data_load_2


def largest_peak_cooling_load(
    _phpp_data_load_1: Dict[str, Unit], _phpp_data_load_2: Dict[str, Unit]
) -> Dict[str, Unit]:
    """Return the largest total (sensible + latent) cooling peak load data-set."""

    peak_sensible_load_1 = _phpp_data_load_1["peak_sensible_cooling_load"]
    peak_sensible_load_2 = _phpp_data_load_2["peak_sensible_cooling_load"]
    peak_latent_load_1 = _phpp_data_load_1["peak_latent_cooling_load"]
    peak_latent_load_2 = _phpp_data_load_2["peak_latent_cooling_load"]

    total_load_1 = peak_sensible_load_1 + peak_latent_load_1
    total_load_2 = peak_sensible_load_2 + peak_latent_load_2

    if total_load_1 > total_load_2:
        return _phpp_data_load_1
    else:
        return _phpp_data_load_2


def build_peak_head_load(
    _phpp_data_load_1: Dict[str, Unit], _phpp_data_load_2: Dict[str, Unit]
) -> performance.NBDM_PeakHeatingLoad:
    """Return a new NBDM.PeakHeatingLoad object based on data from a PHPP."""

    data = largest_peak_heating_load(_phpp_data_load_1, _phpp_data_load_2)
    return performance.NBDM_PeakHeatingLoad.from_phpp_data(data)


def build_peak_cooling_load(
    _phpp_data_load_1: Dict[str, Unit], _phpp_data_load_2: Dict[str, Unit]
) -> performance.NBDM_PeakCoolingLoad:
    """Return a new NBDM.PeakCoolingLoad object based on data from a PHPP."""

    data = largest_peak_cooling_load(_phpp_data_load_1, _phpp_data_load_2)
    return performance.NBDM_PeakCoolingLoad.from_phpp_data(data)


# -----------------------------------------------------------------------------
# -- NBDM Performance


def build_NBDM_performance(_phpp_conn: phpp_app.PHPPConnection):
    """Read in data from a PHPP document and create a new NBDM_Performance Object."""

    # # -- Peak Loads
    peak_heating_load = build_peak_head_load(
        _phpp_conn.heating_load.get_peak_load_1_data(),
        _phpp_conn.heating_load.get_peak_load_2_data(),
    )
    peak_cooling_load = build_peak_cooling_load(
        _phpp_conn.cooling_load.get_peak_load_1_data(),
        _phpp_conn.cooling_load.get_peak_load_2_data(),
    )

    # # -- Annual Demands
    annual_heating_energy_demand = build_annual_heating_demand(
        _phpp_conn.heating.get_annual_demand()
    )
    annual_cooling_energy_demand = build_annual_cooling_demand(
        _phpp_conn.cooling.get_annual_demand()
    )

    # -- Site and Source Energy
    site_energy = build_site_energy(_phpp_conn.per.get_final_kWh_by_fuel_type())
    source_energy = build_source_energy(_phpp_conn.per.get_primary_kWh_by_fuel_type())

    return performance.NBDM_BuildingSegmentPerformance(
        site_energy,
        source_energy,
        annual_heating_energy_demand,
        annual_cooling_energy_demand,
        peak_heating_load,
        peak_cooling_load,
    )
