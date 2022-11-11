from dataclasses import asdict
from NBDM.model.performance import (NBDM_BuildingSegmentPerformance, 
            NBDM_SiteEnergy, NBDM_SourceEnergy, NBDM_AnnualHeatingDemandEnergy, 
            NBDM_AnnualCoolingDemandEnergy, NBDM_PeakHeatingLoad, NBDM_PeakSensibleCoolingLoad)

def test_building_segment_performance(sample_NBDM_BuildingSegmentPerformance):
    assert sample_NBDM_BuildingSegmentPerformance

def test_site_energy_to_dict(sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.site_energy)
    obj = NBDM_SiteEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

def test_source_energy_to_dict(sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.source_energy)
    obj = NBDM_SourceEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

def test_heating_demand_to_dict(sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.annual_heating_energy_demand)
    obj = NBDM_AnnualHeatingDemandEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

def test_cooling_demand_to_dict(sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.annual_cooling_energy_demand)
    obj = NBDM_AnnualCoolingDemandEnergy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

def test_heat_load_to_dict(sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.peak_heating_load)
    obj = NBDM_PeakHeatingLoad.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

def test_cooling_load_to_dict(sample_NBDM_BuildingSegmentPerformance: NBDM_BuildingSegmentPerformance):
    d1 = asdict(sample_NBDM_BuildingSegmentPerformance.peak_sensible_cooling_load)
    obj = NBDM_PeakSensibleCoolingLoad.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2