from NBDM.model import serialization
from copy import copy
from NBDM.model.performance import (
    NBDM_BuildingSegmentPerformance,
    NBDM_SiteEnergy,
    NBDM_SourceEnergy,
    NBDM_AnnualHeatingDemandEnergy,
    NBDM_AnnualCoolingDemandEnergy,
    NBDM_PeakHeatingLoad,
    NBDM_PeakCoolingLoad,
)


def test_building_segment_performance(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    assert sample_NBDM_BuildingSegmentPerformance


def test_site_energy_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = serialization.to_dict(sample_NBDM_BuildingSegmentPerformance.site_energy)
    obj = NBDM_SiteEnergy.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_source_energy_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = serialization.to_dict(sample_NBDM_BuildingSegmentPerformance.source_energy)
    obj = NBDM_SourceEnergy.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_heating_demand_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = serialization.to_dict(
        sample_NBDM_BuildingSegmentPerformance.annual_heating_energy_demand
    )
    obj = NBDM_AnnualHeatingDemandEnergy.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_cooling_demand_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = serialization.to_dict(
        sample_NBDM_BuildingSegmentPerformance.annual_cooling_energy_demand
    )
    obj = NBDM_AnnualCoolingDemandEnergy.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_heat_load_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = serialization.to_dict(sample_NBDM_BuildingSegmentPerformance.peak_heating_load)
    obj = NBDM_PeakHeatingLoad.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_cooling_load_to_dict(
    sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance,
):
    d1 = serialization.to_dict(sample_NBDM_BuildingSegmentPerformance.peak_cooling_load)
    obj = NBDM_PeakCoolingLoad.from_dict(d1)
    d2 = serialization.to_dict(obj)

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
    assert (
        perf_3.annual_heating_energy_demand
        == perf_1.annual_heating_energy_demand + perf_2.annual_heating_energy_demand
    )
    assert (
        perf_3.annual_cooling_energy_demand
        == perf_1.annual_cooling_energy_demand + perf_2.annual_cooling_energy_demand
    )
    assert perf_3.peak_heating_load == perf_1.peak_heating_load + perf_2.peak_heating_load
    assert perf_3.peak_cooling_load == perf_1.peak_cooling_load + perf_2.peak_cooling_load
