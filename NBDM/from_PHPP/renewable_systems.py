# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Renewable Energy Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.renewable_systems import (
    NBDM_BuildingSegmentRenewableSystems,
    NBDM_SolarDHWDevice,
    NBDM_SolarPVDevice,
)


def create_NBDM_Renewable_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentRenewableSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentRenewableSystems Object."""
    system_obj = NBDM_BuildingSegmentRenewableSystems()

    # -------------------------------------------------------------------------
    # -- Solar DHW Device
    solar_dhw_data = _phpp_conn.solar_dhw.get_phpp_data()

    solar_dhw = NBDM_SolarDHWDevice()
    solar_dhw.footprint = solar_dhw_data.footprint
    solar_dhw.annual_dhw_energy = solar_dhw_data.annual_dhw_energy
    solar_dhw.annual_dhw_contribution = solar_dhw_data.annual_dhw_contribution
    solar_dhw.annual_heating_energy = solar_dhw_data.annual_heating_energy
    solar_dhw.annual_heating_contribution = solar_dhw_data.annual_heating_contribution
    system_obj.add_solar_dhw_device(solar_dhw)

    # -------------------------------------------------------------------------
    # -- Solar PV Device(s)
    for solar_pv_data in _phpp_conn.solar_pv.get_phpp_data():
        if solar_pv_data.annual_pv_energy.value < 0.0001:
            continue

        solar_pv = NBDM_SolarPVDevice()
        solar_pv.display_name = solar_pv_data.display_name
        solar_pv.footprint = solar_pv_data.footprint
        solar_pv.size = solar_pv_data.size
        solar_pv.annual_pv_energy = solar_pv_data.annual_pv_energy

        system_obj.add_solar_pv_device(solar_pv)

    return system_obj
