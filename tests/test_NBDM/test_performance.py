from dataclasses import asdict
from copy import copy
from NBDM.model.performance import (
    NBDM_BuildingSegmentPerformance,
    NBDM_SiteEnergy,
    NBDM_SourceEnergy,
    NBDM_AnnualHeatingDemandEnergy,
    NBDM_AnnualCoolingDemandEnergy,
    NBDM_PeakHeatingLoad,
    NBDM_PeakSensibleCoolingLoad,
)


def test_building_segment_performance(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    assert sample_NBDM_BuildingSegmentPerformance


def test_site_energy_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.site_energy)
    obj = NBDM_SiteEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_source_energy_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.source_energy)
    obj = NBDM_SourceEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_heating_demand_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.annual_heating_energy_demand)
    obj = NBDM_AnnualHeatingDemandEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_cooling_demand_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.annual_cooling_energy_demand)
    obj = NBDM_AnnualCoolingDemandEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_heat_load_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.peak_heating_load)
    obj = NBDM_PeakHeatingLoad.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_cooling_load_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.peak_sensible_cooling_load)
    obj = NBDM_PeakSensibleCoolingLoad.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


# --- Tes Additions
def test_add_building_segment_performance(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    perf_1 = copy(sample_NBDM_BuildingSegmentPerformance)
    perf_2 = copy(sample_NBDM_BuildingSegmentPerformance)

    perf_3 = perf_1 + perf_2
    assert perf_3.site_energy == perf_1.site_energy + perf_2.site_energy
    assert perf_3.source_energy == perf_1.source_energy + perf_2.source_energy
    assert perf_3.energy_cost == perf_1.energy_cost + perf_2.energy_cost
    assert (
        perf_3.annual_heating_energy_demand
        == perf_1.annual_heating_energy_demand + perf_2.annual_heating_energy_demand
    )
    assert (
        perf_3.annual_cooling_energy_demand
        == perf_1.annual_cooling_energy_demand + perf_2.annual_cooling_energy_demand
    )
    assert (
        perf_3.peak_heating_load == perf_1.peak_heating_load + perf_2.peak_heating_load
    )
    assert (
        perf_3.peak_sensible_cooling_load
        == perf_1.peak_sensible_cooling_load + perf_2.peak_sensible_cooling_load
    )


def test_add_energy_cost(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    ec1 = copy(sample_NBDM_BuildingSegmentPerformance.energy_cost)
    ec2 = copy(sample_NBDM_BuildingSegmentPerformance.energy_cost)

    ec3 = ec1 + ec2

    assert ec3 is not None
    assert ec3.cost_gas == ec1.cost_gas + ec2.cost_gas
    assert ec3.cost_electricity == ec1.cost_electricity + ec2.cost_electricity
    assert ec3.cost_district_heat == ec1.cost_district_heat + ec2.cost_district_heat
    assert ec3.cost_other_energy == ec1.cost_other_energy + ec2.cost_other_energy


# --- Test Subtractions
def test_subtract_energy_cost(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    ec1 = copy(sample_NBDM_BuildingSegmentPerformance.energy_cost)
    ec2 = copy(sample_NBDM_BuildingSegmentPerformance.energy_cost)

    ec3 = ec1 - ec2

    assert ec3 is not None
    assert ec3.cost_gas == ec1.cost_gas - ec2.cost_gas
    assert ec3.cost_electricity == ec1.cost_electricity - ec2.cost_electricity
    assert ec3.cost_district_heat == ec1.cost_district_heat - ec2.cost_district_heat
    assert ec3.cost_other_energy == ec1.cost_other_energy - ec2.cost_other_energy
