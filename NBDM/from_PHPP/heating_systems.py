# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Heating Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.enums import heating_device_type
from NBDM.model.heating_systems import (
    NBDM_BuildingSegmentHeatingSystems,
    NBDM_HeatingDevice,
)

# -- PHPP type name --> NBDM type
heating_device_type_map = {
    "1-HP compact unit": heating_device_type.COMPACT_HEAT_PUMP,
    "2-Heat pump(s)": heating_device_type.HEAT_PUMP,
    "3-District heating, CHP": heating_device_type.DISTRICT_HEATING,
    "4-Heating boiler": heating_device_type.BOILER,
    "5-Direct electricity": heating_device_type.DIRECT_ELECTRIC,
    "6-Other": heating_device_type.OTHER,
}


def create_NBDM_Heating_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentHeatingSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentHeatingSystems Object."""
    obj = NBDM_BuildingSegmentHeatingSystems()

    for heating_device in _phpp_conn.per.get_heating_device_type_data():
        if heating_device.device_type_name == "-":
            continue
        if heating_device.device_heating_percentage.value <= 0.0001:
            continue

        obj.add_device(
            NBDM_HeatingDevice(
                device_type=heating_device_type_map[heating_device.device_type_name],
                coverage_segment_heating=heating_device.device_heating_percentage,
            )
        )

    return obj
