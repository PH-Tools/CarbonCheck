# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model formatting for user-facing (Excel, GUI, etc) and object field ordering."""

# ------------------------------------------------------------
# -- Project


class Format_NBDM_Project:
    project_name = "Project Name"
    client = "Client"
    report_date = "Report Date"
    site = "Site"
    team = "Team"


# ------------------------------------------------------------
# -- Project Data (Site, Climate)


class Format_NBDM_Site:
    climate = "Climate"
    location = "Location"


class Format_NBDM_Climate:
    country = "Country"
    region = "Region"
    data_set = "Dataset Name"
    zone_passive_house = "Passive House CZ"


class Format_NBDM_Location:
    longitude = "Longitude"
    latitude = "Latitude"
    address = "Address"


class Format_NBDM_ProjectAddress:
    building_number = "Number"
    street_name = "Street"
    city = "City"
    state = "State"
    post_code = "Zipcode"


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
    country = "Country"
    post_code = "Zipcode"
    phone = "Phone"
    email = "Email"


class Format_NBDM_Building:
    building_name = "Building Name"
    building_type = "Building Type"
    geometry = "Geometry"
    occupancy = "Occupancy"
    performance = "Performance"


# ------------------------------------------------------------
# -- Building Segments


class Format_NBDM_BuildingSegment:
    segment_name = "Segment Name"
    construction_type = "Construction Type"
    construction_method = "Construction Method"
    geometry = "Geometry"
    occupancy = "Occupancy"
    performance = "Energy"


class Format_NBDM_BuildingSegmentGeometry:
    area_envelope = "Envelope Area"
    area_floor_area_net_interior_weighted = "Net Interior Floor Area"
    volume_net_interior = "Net Interior Volume"


class Format_NBDM_BuildingSegmentOccupancy:
    total_dwelling_units = "Total Dwelling Units"
    total_occupants = "Total Num. Occupants"


class Format_NBDM_BuildingSegmentPerformance:
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


class Format_NBDM_AnnualHeatingDemandEnergy:
    heating_demand = "Winter Heating Energy Demand"
    losses_transmission = "Transmission Heat Losses"
    losses_ventilation = "Ventilation Heat Losses"
    gains_solar = "Solar Heat Gains"
    gains_internal = "Internal Heat Gains"
    utilization_factor = "Winter Utilization Factor"
    losses_total = "Total Winter Heat Losses"
    gains_total = "Total Winter Useful Heat Gains"


class Format_NBDM_AnnualCoolingDemandEnergy:
    sensible_cooling_demand = "Summer Sensible Cooling Energy Demand"
    latent_cooling_demand = "Summer Latent Cooling Energy Demand"
    total_cooling_demand = "Summer Total Cooling Energy Demand"
    losses_transmission = "Transmission Heat Losses"
    losses_ventilation = "Ventilation Heat Losses"
    gains_solar = "Solar Heat Gains"
    gains_internal = "Internal Heat Gains"
    utilization_factor = "Seasonal Utilization Factor"
    losses_total = "Total Summer Useful Heat Losses"
    gains_total = "Total Summer Heat Gains"


class Format_NBDM_PeakHeatingLoad:
    peak_heating_load = "Peak Heating Load"
    losses_transmission = "Peak Transmission Heat Losses"
    losses_ventilation = "Peak Ventilation Heat Losses"
    gains_solar = "Peak Solar Heat Gains"
    gains_internal = "Peak Internal Heat Gains"
    losses_total = "Total Peak Heat Losses"
    gains_total = "Total Peak Heat Gains"


class Format_NBDM_PeakCoolingLoad:
    peak_sensible_cooling_load = "Peak Sensible Cooling Load"
    peak_latent_cooling_load = "Peak Latent Cooling Load"
    losses_transmission = "Peak Transmission Heat Losses"
    losses_ventilation = "Peak Ventilation Heat Losses"
    gains_solar = "Peak Solar Heat Gains"
    gains_internal = "Peak Internal Heat Gains"
    losses_total = "Total Peak Sensible Cooling Losses"
    gains_total = "Total Peak Sensible Cooling Gains"


# ------------------------------------------------------------
# -- Building Specifications


class Format_NBDM_AssemblyType:
    name = "Assembly Type"
    u_value = "U-Value"
    r_value = "R-Value"
    ext_exposure = "Exterior Exposure"
    int_exposure = "Interior Exposure"


class Format_NBDM_ApertureType:
    name = "Window Type"
    u_value = "U-Value"


class Format_NBDM_GlazingType:
    display_name = "Glazing Type"
    u_value = "U-Value"
    g_value = "SHGC"


class Format_NBDM_Appliance:
    display_name = "Device"
    appliance_type = "Type Number"
    quantity = "Quantity"
    annual_energy_use = "Annual Energy Use"


class Format_NBDM_HeatingDevice:
    device_type = "Device Type"
    _display_name = "Name"
    coverage_segment_heating = "Heating % Covered"
    coverage_segment_cooling = "Cooling % Covered"


class Format_NBDM_CoolingDevice:
    device_type = "Device Type"
    cooling_device_name = "Device"
    SEER = "SEER"
    num_units = "Quantity"


class Format_NBDM_VentilationDevice:
    display_name = "Device Name"
    vent_unit_type_name = "Ventilator Unit Type"
    quantity = "Quantity"
    hr_efficiency = "Heat Recovery Efficiency"
    mr_efficiency = "Moisture Recovery Efficiency"


class Format_NBDM_DHWHeatingDevice:
    device_type = "Device Type"
    coverage_segment_hot_water = "Hot Water % Covered"


class Format_NBDM_DHWTankDevice:
    display_name = "Name"
    heat_loss_rate = "Heat Loss Rate"
    volume = "Volume"


class Format_NBDM_SolarDHWDevice:
    footprint = "Footprint"
    annual_dhw_energy = "Hot-Water Energy"
    annual_dhw_contribution = "How Water Contribution"
    annual_heating_energy = "Heating Energy"
    annual_heating_contribution = "Heating Contribution"


class Format_NBDM_SolarPVDevice:
    display_name = "Name"
    footprint = "Footprint"
    size = "Array Size"
    annual_pv_energy = "PV Energy"
