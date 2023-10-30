# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Domestic Hot-Water (DHW) Systems from WUFI-PDF."""

from typing import List, Dict

from NBDM.model.dhw_systems import (
    NBDM_BuildingSegmentDHWSystems,
    NBDM_DHWHeatingDevice,
    NBDM_DHWTankDevice,
)
from NBDM.model.enums import heating_device_type
from NBDM.from_WUFI_PDF.pdf_reader import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC


# -- WUFI type name --> NBDM type
device_map = {
    "1-HP compact unit": heating_device_type.COMPACT_HEAT_PUMP,
    "2-Heat pump(s)": heating_device_type.HEAT_PUMP,
    "3-District heating, CHP": heating_device_type.DISTRICT_HEATING,
    "4-Heating boiler": heating_device_type.BOILER,
    "5-Direct electricity": heating_device_type.DIRECT_ELECTRIC,
    "6-Other": heating_device_type.OTHER,
}


def create_NBDM_DHW_Systems_from_WufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType]
) -> NBDM_BuildingSegmentDHWSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentDHWSystems Object."""
    obj = NBDM_BuildingSegmentDHWSystems()

    pdf_hvac_data: WufiPDF_HVAC
    if pdf_hvac_data := _pdf_data[WufiPDF_HVAC.__pdf_heading_string__]:
        for pdf_dhw_tank_device_data in pdf_hvac_data.dhw_tank_devices:
            new_vent_unit = NBDM_DHWTankDevice(
                display_name=pdf_dhw_tank_device_data.device_name,
                heat_loss_rate=pdf_dhw_tank_device_data.tank_heat_loss,
                volume=pdf_dhw_tank_device_data.storage_capacity,
            )
            obj.add_tank_device(new_vent_unit)

    return obj
