# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Domestic Hot-Water (DHW) Systems from WUFI-PDF."""


from NBDM.model.dhw_systems import (
    NBDM_BuildingSegmentDHWSystems,
    NBDM_DHWHeatingDevice,
    NBDM_DHWTankDevice,
)
from NBDM.model.enums import heating_device_type


# -- WUFI type name --> NBDM type
device_map = {
    "1-HP compact unit": heating_device_type.COMPACT_HEAT_PUMP,
    "2-Heat pump(s)": heating_device_type.HEAT_PUMP,
    "3-District heating, CHP": heating_device_type.DISTRICT_HEATING,
    "4-Heating boiler": heating_device_type.BOILER,
    "5-Direct electricity": heating_device_type.DIRECT_ELECTRIC,
    "6-Other": heating_device_type.OTHER,
}


def create_NBDM_DHW_Systems_from_WufiPDF(_pdf_data) -> NBDM_BuildingSegmentDHWSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentDHWSystems Object."""
    obj = NBDM_BuildingSegmentDHWSystems()

    return obj
