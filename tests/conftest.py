# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

import pytest

from NBDM.model.building import NBDM_Building, NBDM_BuildingSegment
from NBDM.model.geometry import NBDM_BuildingSegmentGeometry
from NBDM.model.occupancy import NBDM_BuildingSegmentOccupancy
from NBDM.model.performance import (
    NBDM_BuildingSegmentPerformance,
    NBDM_SiteEnergy,
    NBDM_SourceEnergy,
    NBDM_AnnualHeatingDemandEnergy,
    NBDM_AnnualCoolingDemandEnergy,
    NBDM_PeakHeatingLoad,
    NBDM_PeakSensibleCoolingLoad,
)
from NBDM.model.project import NBDM_Project, NBDM_Variant, NBDM_Variants
from NBDM.model.site import NBDM_Climate, NBDM_Location, NBDM_Site, NBDM_ProjectAddress
from NBDM.model.team import NBDM_Team, NBDM_TeamContactInfo, NBDM_TeamMember
from NBDM.model import enums

# -- Project Site -------------------------------------------------------------


sample_ProjectAddress = NBDM_ProjectAddress(
    building_number="486",
    street_name="3rd Ave.",
    city="Brooklyn",
    state="NY",
    zip_code="11215",
)

sample_ProjectClimate = NBDM_Climate(
    zone_ashrae="4a",
    zone_passive_house="4",
    source="The internet",
)

sample_ProjectLocation = NBDM_Location(
    address=sample_ProjectAddress,
    longitude=-73.2,
    latitude=40.1,
)

sample_Site = NBDM_Site(
    climate=sample_ProjectClimate,
    location=sample_ProjectLocation,
)


@pytest.fixture
def sample_NBDM_Site() -> NBDM_Site:
    return sample_Site


# -- Building Segment Occupancy -----------------------------------------------


sample_BuildingSegmentOccupancy_A = NBDM_BuildingSegmentOccupancy(
    total_dwelling_units=2,
    num_apartments_studio=2,
    num_apartments_1_br=1,
    num_apartments_2_br=2,
    num_apartments_3_br=2,
    num_apartments_4_br=2,
    total_occupants=10,
)
sample_BuildingSegmentOccupancy_B = NBDM_BuildingSegmentOccupancy(
    total_dwelling_units=1,
    num_apartments_studio=2,
    num_apartments_1_br=3,
    num_apartments_2_br=4,
    num_apartments_3_br=5,
    num_apartments_4_br=6,
    total_occupants=23,
)


@pytest.fixture
def sample_NBDM_BuildingSegmentOccupancy() -> NBDM_BuildingSegmentOccupancy:
    return sample_BuildingSegmentOccupancy_A


# -- Building Segment Geometry ------------------------------------------------


sample_BuildingSegmentGeometry = NBDM_BuildingSegmentGeometry(
    area_envelope=100.0,
    area_floor_area_gross=100.0,
    area_floor_area_net_interior_weighted=113.0,
    area_floor_area_interior_parking=114.0,
    volume_gross=115.0,
    volume_net_interior=116.0,
    total_stories=8,
    num_stories_above_grade=7,
    num_stories_below_grade=1,
)


@pytest.fixture
def sample_NBDM_BuildingSegmentGeometry() -> NBDM_BuildingSegmentGeometry:
    return sample_BuildingSegmentGeometry


# -- Building Segment Performance ---------------------------------------------


sample_SiteEnergy = NBDM_SiteEnergy(
    consumption_gas=0.0,
    consumption_electricity=0.0,
    consumption_district_heat=0.0,
    consumption_other=0.0,
    production_solar_photovoltaic=0.0,
    production_solar_thermal=0.0,
    production_other=0.0,
)

sample_SourceEnergy = NBDM_SourceEnergy(
    consumption_gas=0.0,
    consumption_electricity=0.0,
    consumption_district_heat=0.0,
    consumption_other=0.0,
    production_solar_photovoltaic=0.0,
    production_solar_thermal=0.0,
    production_other=0.0,
)

sample_AnnualHeatingDemand = NBDM_AnnualHeatingDemandEnergy(
    annual_demand=0.0,
    losses_transmission=0.0,
    losses_ventilation=0.0,
    gains_solar=0.0,
    gains_internal=0.0,
    utilization_factor=0.0,
    gains_useful=0.0,
)

sample_AnnualCoolingDemand = NBDM_AnnualCoolingDemandEnergy(
    annual_demand=0.0,
    losses_transmission=0.0,
    losses_ventilation=0.0,
    utilization_factor=0.0,
    losses_useful=0.0,
    gains_solar=0.0,
    gains_internal=0.0,
)

sample_PeakHeatingLoad = NBDM_PeakHeatingLoad(
    peak_load=0.0,
    losses_transmission=0.0,
    losses_ventilation=0.0,
    gains_solar=0.0,
    gains_internal=0.0,
)

sample_PeakSensibleCoolingLoad = NBDM_PeakSensibleCoolingLoad(
    peak_load=0.0,
    losses_transmission=0.0,
    losses_ventilation=0.0,
    gains_solar=0.0,
    gains_internal=0.0,
)

sample_BuildingSegmentPerformance = NBDM_BuildingSegmentPerformance(
    site_energy=sample_SiteEnergy,
    source_energy=sample_SourceEnergy,
    annual_heating_energy_demand=sample_AnnualHeatingDemand,
    annual_cooling_energy_demand=sample_AnnualCoolingDemand,
    peak_heating_load=sample_PeakHeatingLoad,
    peak_sensible_cooling_load=sample_PeakSensibleCoolingLoad,
)


@pytest.fixture
def sample_NBDM_BuildingSegmentPerformance() -> NBDM_BuildingSegmentPerformance:
    return sample_BuildingSegmentPerformance


# -- Building -----------------------------------------------------------------


sample_BuildingSegment_A = NBDM_BuildingSegment(
    segment_name="A First Bldg Segment",
    geometry=sample_BuildingSegmentGeometry,
    occupancy=sample_BuildingSegmentOccupancy_A,
    performance=sample_BuildingSegmentPerformance,
)

sample_BuildingSegment_B = NBDM_BuildingSegment(
    segment_name="A Different Bldg Segment",
    geometry=sample_BuildingSegmentGeometry,
    occupancy=sample_BuildingSegmentOccupancy_B,
    performance=sample_BuildingSegmentPerformance,
)

sample_Building = NBDM_Building(
    building_name="A Sample Building",
    building_type=enums.building_type.MULTIFAMILY,
)
sample_Building.add_building_segment(sample_BuildingSegment_A)
sample_Building.add_building_segment(sample_BuildingSegment_B)


@pytest.fixture
def sample_NBDM_Building() -> NBDM_Building:
    return sample_Building


# -- Team ---------------------------------------------------------------------

sample_contact_a = NBDM_TeamContactInfo(
    building_number="str",
    street_name="str",
    city="str",
    state="str",
    zip_code="str",
    phone="str",
    email="str",
)

sample_team_member_a = NBDM_TeamMember(
    name="A sample team member",
    contact_info=sample_contact_a,
)

sample_Team = NBDM_Team(
    site_owner=sample_team_member_a,
    designer=sample_team_member_a,
    contractor=sample_team_member_a,
    primary_energy_consultant=sample_team_member_a,
)


# -- Project ------------------------------------------------------------------


sample_Variant = NBDM_Variant(
    variant_name="",
    building=sample_Building,
)

sample_Variants = NBDM_Variants(
    proposed=sample_Variant,
    baseline=sample_Variant,
)

sample_Project = NBDM_Project(
    project_name="A Test Project Name",
    client="A Test Client Name",
    salesforce_num="0123-4567-89",
    report_date="Some Date",
    site=sample_Site,
    team=sample_Team,
    variants=sample_Variants,
)


@pytest.fixture
def sample_NBDM_Project() -> NBDM_Project:
    return sample_Project
