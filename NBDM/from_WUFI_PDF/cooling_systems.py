# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Cooling Systems from WUFI-PDF."""


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


def create_NBDM_Cooling_Systems_from_WufiPDF(
    _pdf_data,
) -> NBDM_BuildingSegmentCoolingSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentCoolingSystems Object."""
    obj = NBDM_BuildingSegmentCoolingSystems()

    return obj
