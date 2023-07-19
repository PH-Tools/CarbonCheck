# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

import pytest

from ph_units.unit_type import Unit

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
    NBDM_PeakCoolingLoad,
)
from NBDM.model.project import NBDM_Project, NBDM_Variant, NBDM_Variants
from NBDM.model.site import NBDM_Climate, NBDM_Location, NBDM_Site, NBDM_ProjectAddress
from NBDM.model.team import NBDM_Team, NBDM_TeamContactInfo, NBDM_TeamMember
from NBDM.model import enums

# -- Project Site -------------------------------------------------------------


sample_ProjectAddress = NBDM_ProjectAddress(
    building_number="99",
    street_name="Example St.",
    city="Example City",
    state="NY",
    post_code="11111",
)

sample_ProjectClimate = NBDM_Climate(
    zone_passive_house="4",
    country="-",
    region="-",
    data_set="",
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
    total_occupants=10.0,
)

sample_BuildingSegmentOccupancy_B = NBDM_BuildingSegmentOccupancy(
    total_dwelling_units=1,
    total_occupants=23.0,
)


@pytest.fixture
def sample_NBDM_BuildingSegmentOccupancy() -> NBDM_BuildingSegmentOccupancy:
    return sample_BuildingSegmentOccupancy_A


# -- Building Segment Geometry ------------------------------------------------


sample_BuildingSegmentGeometry = NBDM_BuildingSegmentGeometry(
    area_envelope=Unit(100.0, "M2"),
    area_floor_area_net_interior_weighted=Unit(113.0, "M2"),
    volume_net_interior=Unit(116.0, "M2"),
)


@pytest.fixture
def sample_NBDM_BuildingSegmentGeometry() -> NBDM_BuildingSegmentGeometry:
    return sample_BuildingSegmentGeometry


# -- Building Segment Performance ---------------------------------------------


sample_SiteEnergy = NBDM_SiteEnergy(
    consumption_gas=Unit(0.0, "KWH"),
    consumption_electricity=Unit(0.0, "KWH"),
    consumption_district_heat=Unit(0.0, "KWH"),
    consumption_other=Unit(0.0, "KWH"),
    production_solar_photovoltaic=Unit(0.0, "KWH"),
    production_solar_thermal=Unit(0.0, "KWH"),
    production_other=Unit(0.0, "KWH"),
)

sample_SourceEnergy = NBDM_SourceEnergy(
    consumption_gas=Unit(0.0, "KWH"),
    consumption_electricity=Unit(0.0, "KWH"),
    consumption_district_heat=Unit(0.0, "KWH"),
    consumption_other=Unit(0.0, "KWH"),
    production_solar_photovoltaic=Unit(0.0, "KWH"),
    production_solar_thermal=Unit(0.0, "KWH"),
    production_other=Unit(0.0, "KWH"),
)


sample_AnnualHeatingDemand = NBDM_AnnualHeatingDemandEnergy(
    heating_demand=Unit(0.0, "KWH"),
    losses_transmission=Unit(0.0, "KWH"),
    losses_ventilation=Unit(0.0, "KWH"),
    gains_solar=Unit(0.0, "KWH"),
    gains_internal=Unit(0.0, "KWH"),
    utilization_factor=Unit(0.0, "KWH"),
)

sample_AnnualCoolingDemand = NBDM_AnnualCoolingDemandEnergy(
    sensible_cooling_demand=Unit(0.0, "KWH"),
    latent_cooling_demand=Unit(0.0, "KWH"),
    losses_transmission=Unit(0.0, "KWH"),
    losses_ventilation=Unit(0.0, "KWH"),
    utilization_factor=Unit(0.0, "KWH"),
    gains_solar=Unit(0.0, "KWH"),
    gains_internal=Unit(0.0, "KWH"),
)

sample_PeakHeatingLoad = NBDM_PeakHeatingLoad(
    peak_heating_load=Unit(0.0, "W"),
    losses_transmission=Unit(0.0, "W"),
    losses_ventilation=Unit(0.0, "W"),
    gains_solar=Unit(0.0, "W"),
    gains_internal=Unit(0.0, "W"),
)

sample_PeakSensibleCoolingLoad = NBDM_PeakCoolingLoad(
    peak_sensible_cooling_load=Unit(0.0, "W"),
    peak_latent_cooling_load=Unit(0.0, "W"),
    losses_transmission=Unit(0.0, "W"),
    losses_ventilation=Unit(0.0, "W"),
    gains_solar=Unit(0.0, "W"),
    gains_internal=Unit(0.0, "W"),
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
    segment_name="Residential Segment",
    construction_type=enums.construction_type.NEW_CONSTRUCTION,
    construction_method=enums.construction_method.METHOD_A,
    geometry=sample_BuildingSegmentGeometry,
    occupancy=sample_BuildingSegmentOccupancy_A,
    performance=sample_BuildingSegmentPerformance,
)

sample_BuildingSegment_B = NBDM_BuildingSegment(
    segment_name="Commercial Segment",
    construction_type=enums.construction_type.NEW_CONSTRUCTION,
    construction_method=enums.construction_method.METHOD_A,
    geometry=sample_BuildingSegmentGeometry,
    occupancy=sample_BuildingSegmentOccupancy_B,
    performance=sample_BuildingSegmentPerformance,
)

sample_Building = NBDM_Building(
    building_name="Example Building",
    building_type=enums.building_type.MULTIFAMILY,
)

sample_Building.add_building_segment(sample_BuildingSegment_A)
sample_Building.add_building_segment(sample_BuildingSegment_B)


@pytest.fixture
def sample_NBDM_Building() -> NBDM_Building:
    return sample_Building


# -- Team ---------------------------------------------------------------------

sample_contact_a = NBDM_TeamContactInfo(
    building_number="99",
    street_name="Example Street",
    city="Example City",
    state="NY",
    post_code="11111",
    phone="555-555-5555",
    email="example@email.com",
)

sample_team_member_a = NBDM_TeamMember(
    name="Example Team Member",
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
    report_date="Some Date",
    site=sample_Site,
    team=sample_Team,
    variants=sample_Variants,
)


@pytest.fixture
def sample_NBDM_Project() -> NBDM_Project:
    return sample_Project
