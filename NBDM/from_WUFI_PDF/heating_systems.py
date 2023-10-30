# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Heating Systems from WUFI-PDF."""

from typing import Dict

from NBDM.model.heating_systems import (
    NBDM_BuildingSegmentHeatingSystems,
    NBDM_HeatingDevice,
)
from NBDM.model.enums import heating_device_type

from NBDM.from_WUFI_PDF.pdf_reader import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC

# -- PHPP type name --> NBDM type
heating_device_type_map = {
    "1-HP compact unit": heating_device_type.COMPACT_HEAT_PUMP,
    "2-Heat pump(s)": heating_device_type.HEAT_PUMP,
    "3-District heating, CHP": heating_device_type.DISTRICT_HEATING,
    "4-Heating boiler": heating_device_type.BOILER,
    "5-Direct electricity": heating_device_type.DIRECT_ELECTRIC,
    "6-Other": heating_device_type.OTHER,
}


def create_NBDM_Heating_Systems_from_WufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType],
) -> NBDM_BuildingSegmentHeatingSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentHeatingSystems Object."""
    obj = NBDM_BuildingSegmentHeatingSystems()

    # heating_system_data: WufiPDF_HVAC
    # if heating_system_data := _pdf_data[WufiPDF_HVAC.__pdf_heading_string__]:
    #     for pdf_device_data in heating_system_data.ventilation_devices:
    #         pass
    # new_heating_device = NBDM_HeatingDevice()
    # obj.add_device(new_heating_device)

    return obj
