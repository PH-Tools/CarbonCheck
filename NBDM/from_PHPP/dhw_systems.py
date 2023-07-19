# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Domestic Hot-Water (DHW) Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.dhw_systems import (
    NBDM_BuildingSegmentDHWSystems,
    NBDM_DHWHeatingDevice,
    NBDM_DHWTankDevice,
)
from NBDM.model.enums import heating_device_type


# -- PHPP type name --> NBDM type
device_map = {
    "1-HP compact unit": heating_device_type.COMPACT_HEAT_PUMP,
    "2-Heat pump(s)": heating_device_type.HEAT_PUMP,
    "3-District heating, CHP": heating_device_type.DISTRICT_HEATING,
    "4-Heating boiler": heating_device_type.BOILER,
    "5-Direct electricity": heating_device_type.DIRECT_ELECTRIC,
    "6-Other": heating_device_type.OTHER,
}


def create_NBDM_DHW_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentDHWSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentDHWSystems Object."""
    obj = NBDM_BuildingSegmentDHWSystems()

    for heating_device in _phpp_conn.per.get_heating_device_type_data():
        if heating_device.device_type_name == "-":
            continue
        if heating_device.device_dhw_percentage.value <= 0.0001:
            continue

        obj.add_heating_device(
            NBDM_DHWHeatingDevice(
                device_type=device_map[heating_device.device_type_name],
                coverage_segment_hot_water=heating_device.device_dhw_percentage,
            )
        )

    for i, tank_device in enumerate(_phpp_conn.hot_water.get_all_tank_device_data()):
        print(">", tank_device.type)

        if str(tank_device.type).startswith("0"):
            continue

        tank = NBDM_DHWTankDevice()
        tank.display_name = f"Tank {i+1}"
        tank.heat_loss_rate = tank_device.heat_loss_rate
        tank.volume = tank_device.volume

        obj.add_tank_device(tank)

    return obj
