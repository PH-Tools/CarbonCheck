# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Ventilation Systems from WUFI-PDF."""

from typing import Dict

from NBDM.model.ventilation_systems import (
    NBDM_BuildingSegmentVentilationSystems,
    NBDM_VentilationDevice,
)

from NBDM.from_WUFI_PDF.pdf_reader import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC


def create_NBDM_Vent_Systems_from_WufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType],
) -> NBDM_BuildingSegmentVentilationSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentVentilationSystems Object."""
    obj = NBDM_BuildingSegmentVentilationSystems()

    pdf_hvac_data: WufiPDF_HVAC
    if pdf_hvac_data := _pdf_data[WufiPDF_HVAC.__pdf_heading_string__]:
        for pdf_vent_device_data in pdf_hvac_data.ventilation_devices:
            new_vent_unit = NBDM_VentilationDevice(
                display_name=pdf_vent_device_data.device_name,
                vent_unit_type_name=pdf_vent_device_data.device_name,
                quantity=pdf_vent_device_data.quantity,
                hr_efficiency=pdf_vent_device_data.sensible_recovery,
                mr_efficiency=pdf_vent_device_data.moisture_recovery,
            )
            obj.add_device(new_vent_unit)

    return obj
