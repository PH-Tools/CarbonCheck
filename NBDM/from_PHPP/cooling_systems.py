# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Cooling Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection
from PHX.model.enums.hvac import CoolingType

from NBDM.model.enums import cooling_device_type
from NBDM.model.cooling_systems import (
    NBDM_BuildingSegmentCoolingSystems,
    NBDM_CoolingDevice,
)

device_map = {
    CoolingType.NONE: cooling_device_type.NONE,
    CoolingType.VENTILATION: cooling_device_type.SUPPLY_AIR,
    CoolingType.RECIRCULATION: cooling_device_type.RECIRCULATION_AIR,
    CoolingType.DEHUMIDIFICATION: cooling_device_type.DEHUMIDIFICATION,
    CoolingType.PANEL: cooling_device_type.PANEL,
}


def create_NBDM_Cooling_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentCoolingSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentCoolingSystems Object."""
    obj = NBDM_BuildingSegmentCoolingSystems()

    for phpp_cooling_system in _phpp_conn.cooling_units.get_cooling_system_data():
        if not phpp_cooling_system.used:
            continue

        obj.add_device(
            NBDM_CoolingDevice(
                device_type=device_map[phpp_cooling_system.device_type],
                cooling_device_name=phpp_cooling_system.device_type_name or "",
                SEER=phpp_cooling_system.SEER,
                num_units=phpp_cooling_system.num_units,
            )
        )

    return obj
