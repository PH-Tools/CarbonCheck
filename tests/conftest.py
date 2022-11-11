# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

import pytest

from NBDM.model.building import NBDM_Building, NBDM_BuildingSegment
from NBDM.model.geometry import NBDM_BuildingSegmentGeometry
from NBDM.model.occupancy import NBDM_BuildingSegmentOccupancy
from NBDM.model.performance import (NBDM_BuildingSegmentPerformance, NBDM_SiteEnergy, 
    NBDM_SourceEnergy, NBDM_AnnualHeatingDemandEnergy, NBDM_AnnualCoolingDemandEnergy,
    NBDM_PeakHeatingLoad, NBDM_PeakSensibleCoolingLoad)
from NBDM.model.project import NBDM_Project, NBDM_Variant, NBDM_Variants
from NBDM.model.site import NBDM_Climate, NBDM_Location, NBDM_Site, NBDM_ProjectAddress


# -- Project Site -------------------------------------------------------------


sample_ProjectAddress = NBDM_ProjectAddress(
    number = "",
    street = "",
    city = "",
    state = "",
    zip_code = "",
)

sample_ProjectClimate = NBDM_Climate(
    zone_ashrae = 0,
    zone_passive_house = 0,
    source = "",
)

sample_ProjectLocation = NBDM_Location(
    address = sample_ProjectAddress,
    longitude = 0.0,
    latitude = 0.0,
)

sample_Site = NBDM_Site(
        climate = sample_ProjectClimate,
        location = sample_ProjectLocation,
    )

@pytest.fixture
def sample_NBDM_Site() -> NBDM_Site:
    return sample_Site


# -- Building Segment Occupancy -----------------------------------------------


sample_BuildingSegmentOccupancy = NBDM_BuildingSegmentOccupancy(
        total_dwelling_units = 0,
        num_apartments_studio = 0,
        num_apartments_1_br = 0,
        num_apartments_2_br = 0,
        num_apartments_3_br = 0,
        num_apartments_4_br = 0,
        total_occupants = 0,
    )

@pytest.fixture
def sample_NBDM_BuildingSegmentOccupancy() -> NBDM_BuildingSegmentOccupancy:
    return sample_BuildingSegmentOccupancy


# -- Building Segment Geometry ------------------------------------------------


sample_BuildingSegmentGeometry = NBDM_BuildingSegmentGeometry(
        area_envelope = 0.0,
        area_floor_area_gross = 0.0,
        area_floor_area_net_interior_weighted = 0.0,
        area_floor_area_interior_parking = 0.0,
        volume_gross = 0.0,
        volume_net_interior = 0.0,
        total_stories = 0,
        num_stories_above_grade = 0,
        num_stories_below_grade = 0,
    )

@pytest.fixture
def sample_NBDM_BuildingSegmentGeometry() -> NBDM_BuildingSegmentGeometry:
    return sample_BuildingSegmentGeometry


# -- Building Segment Performance ---------------------------------------------


sample_SiteEnergy = NBDM_SiteEnergy(
        consumption_gas = 0.0,
        consumption_electricity = 0.0,
        consumption_district_heat = 0.0,
        consumption_other = 0.0,
        production_solar_photovoltaic = 0.0,
        production_solar_thermal = 0.0,
        production_other = 0.0,
    )

sample_SourceEnergy = NBDM_SourceEnergy(
        consumption_gas = 0.0,
        consumption_electricity = 0.0,
        consumption_district_heat = 0.0,
        consumption_other = 0.0,
        production_solar_photovoltaic = 0.0,
        production_solar_thermal = 0.0,
        production_other = 0.0,
    )

sample_AnnualHeatingDemand = NBDM_AnnualHeatingDemandEnergy(
    annual_demand = 0.0,
    losses_transmission = 0.0,
    losses_ventilation = 0.0,
    gains_solar = 0.0,
    gains_internal = 0.0,
    utilization_factor = 0.0,
    gains_useful = 0.0,
)

sample_AnnualCoolingDemand = NBDM_AnnualCoolingDemandEnergy(
    annual_demand = 0.0,
    losses_transmission = 0.0,
    losses_ventilation = 0.0,
    utilization_factor = 0.0,
    losses_useful = 0.0,
    gains_solar = 0.0,
    gains_internal = 0.0,
)

sample_PeakHeatingLoad = NBDM_PeakHeatingLoad(
    peak_load = 0.0,
    losses_transmission = 0.0,
    losses_ventilation = 0.0,
    gains_solar = 0.0,
    gains_internal = 0.0,
    utilization_factor = 0.0,
    gains_useful = 0.0,
 )

sample_PeakSensibleCoolingLoad = NBDM_PeakSensibleCoolingLoad(
    peak_load = 0.0,
    losses_transmission = 0.0,
    losses_ventilation = 0.0,
    utilization_factor = 0.0,
    losses_useful = 0.0,
    gains_solar = 0.0,
    gains_internal = 0.0,
 )

sample_BuildingSegmentPerformance = NBDM_BuildingSegmentPerformance(
        site_energy = sample_SiteEnergy,
        source_energy = sample_SourceEnergy,
        annual_heating_energy_demand = sample_AnnualHeatingDemand,
        annual_cooling_energy_demand = sample_AnnualCoolingDemand,
        peak_heating_load = sample_PeakHeatingLoad,
        peak_sensible_cooling_load = sample_PeakSensibleCoolingLoad,
    )

@pytest.fixture
def sample_NBDM_BuildingSegmentPerformance() -> NBDM_BuildingSegmentPerformance:
    return sample_BuildingSegmentPerformance


# -- Building -----------------------------------------------------------------


sample_BuildingSegment = NBDM_BuildingSegment(
    segment_name = "",
    geometry = sample_BuildingSegmentGeometry,
    occupancy = sample_BuildingSegmentOccupancy,
    performance = sample_BuildingSegmentPerformance,
)

sample_Building = NBDM_Building(
    building_name = "", 
)
sample_Building.add_building_segment(sample_BuildingSegment)

@pytest.fixture
def sample_NBDM_Building() -> NBDM_Building:
    return sample_Building


# -- Project ------------------------------------------------------------------


sample_Variant = NBDM_Variant(
    variant_name = "",
    building = sample_Building,
)

sample_Variants = NBDM_Variants(
    proposed = sample_Variant,
    baseline = sample_Variant,
)

sample_Project = NBDM_Project(
    project_name = "test_proejct_name",
    client = "test_client_name",
    site = sample_Site,
    variants = sample_Variants,
)

@pytest.fixture
def sample_NBDM_Project() -> NBDM_Project:
    return sample_Project
