# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model formatting for user-facing (Excel, GUI, etc) and object field ordering."""


class Format_NBDM_Project:
    project_name = "Project Name"
    client = "Client"
    salesforce_num = "SalesForce Number"
    report_date = "Report Date"
    nyc_ecc_year = "NYC ECC Year"
    historic_preservation_site = "Historic Preservation Site"
    disadvantaged_communities = "Disadvantaged Communities"
    site = "Site"
    team = "Team"


class Format_NBDM_Site:
    climate = "Climate"
    location = "Location"


class Format_NBDM_Climate:
    zone_ashrae = "ASHRAE CZ"
    zone_passive_house = "Passive House CZ"
    source = "Climate Data Source"


class Format_NBDM_Location:
    longitude = "Longitude"
    latitude = "Latitude"
    address = "Address"


class Format_NBDM_ProjectAddress:
    building_number = "Number"
    street_name = "Street"
    city = "City"
    state = "State"
    zip_code = "Zip_code"


class Format_NBDM_Team:
    site_owner = "Owner"
    designer = "Designer"
    contractor = "Contractor"
    primary_energy_consultant = "Primary Energy Consultant"


class Format_NBDM_TeamMember:
    name = "Name"
    contact_info = "Contact"


class Format_NBDM_TeamContactInfo:
    building_number = "Num."
    street_name = "Street"
    city = "City"
    state = "State"
    zip_code = "Zip"
    phone = "Phone"
    email = "Email"


class Format_NBDM_Building:
    building_name = "Building Name"
    building_type = "Building Type"
    geometry = "Geometry"
    occupancy = "Occupancy"
    performance = "Performance"


class Format_NBDM_BuildingSegment:
    segment_name = "Segment Name"
    construction_type = "Construction Type"
    construction_method = "Construction Method"
    geometry = "Geometry"
    occupancy = "Occupancy"
    performance = "Energy"


class Format_NBDM_BuildingSegmentGeometry:
    area_envelope = "Envelope Area"
    area_floor_area_gross = "Gross Floor Area"
    area_floor_area_net_interior_weighted = "Net Interior Floor Area"
    area_floor_area_interior_parking = "Interior Parking Floor Area"
    volume_gross = "Gross Volume"
    volume_net_interior = "Net Interior Volume"
    total_stories = "Num. Stories"
    num_stories_above_grade = "Num. Stories Above Grade"
    num_stories_below_grade = "Num. Stories Below Grade"


class Format_NBDM_BuildingSegmentOccupancy:
    total_dwelling_units = "Total Dwelling Units"
    num_apartments_studio = "Num. Studio"
    num_apartments_1_br = "Num. 1Br"
    num_apartments_2_br = "Num. 2Br"
    num_apartments_3_br = "Num. 3Br"
    num_apartments_4_br = "Num. 4Br"
    total_occupants = "Total Num. Occupants"


class Format_NBDM_BuildingSegmentPerformance:
    energy_cost = "Annual Energy Cost (USD)"
    site_energy = "Annual Site (End) Energy"
    source_energy = "Annual Source (Primary) Energy"
    annual_heating_energy_demand = "Annual Heating Demand"
    annual_cooling_energy_demand = "Annual Cooling Demand"
    peak_heating_load = "Peak Heating Load"
    peak_sensible_cooling_load = "Peak Cooling Load"


class Format_NBDM_SiteEnergy:
    consumption_gas = "Consumption: Gas"
    consumption_electricity = "Consumption: Electricity"
    consumption_district_heat = "Consumption: District Energy"
    consumption_other = "Consumption: Other"
    production_solar_photovoltaic = "Production: Solar PV"
    production_solar_thermal = "Production Solar Thermal"
    production_other = "Production Other"


class Format_NBDM_SourceEnergy:
    consumption_gas = "Consumption: Gas"
    consumption_electricity = "Consumption: Electricity"
    consumption_district_heat = "Consumption: District Energy"
    consumption_other = "Consumption: Other"
    production_solar_photovoltaic = "Production: Solar PV"
    production_solar_thermal = "Production Solar Thermal"
    production_other = "Production Other"


class Format_NBDM_EnergyCost:
    cost_gas = "Cost: Gas"
    cost_electricity = "Cost: Electricity"
    cost_district_heat = "Cost: District Energy"
    cost_other_energy = "Cost: Other"


class Format_NBDM_AnnualHeatingDemandEnergy:
    heating_demand = "Annual Heating Energy Demand"
    losses_total = "Winter Heat Losses"
    gains_total = "Winter Useful Heat Gains"


class Format_NBDM_AnnualCoolingDemandEnergy:
    sensible_cooling_demand = "Annual Sensible Cooling Energy Demand"
    latent_cooling_demand = "Annual Latent Cooling Energy Demand"
    losses_total = "Summer Useful Heat Losses"
    gains_total = "Summer Heat Gains"


class Format_NBDM_PeakHeatingLoad:
    peak_load = "Peak Heating Load"
    losses_total = "Total Peak Heat Losses"
    gains_total = "Total Peak Heat Gains"


class Format_NBDM_PeakCoolingLoad:
    peak_load_sensible = "Peak Sensible Cooling Load"
    peak_load_latent = "Peak Latent Cooling Load"
    losses_total = "Total Peak Sensible Cooling Losses"
    gains_total = "Total Peak Sensible Cooling Gains"
