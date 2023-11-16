# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Heating Systems from WUFI-PDF."""


from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC

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


def create_NBDM_Heating_Systems_from_WufiPDF(
    _pdf_data: PDFSectionsCollection,
) -> NBDM_BuildingSegmentHeatingSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentHeatingSystems Object."""
    obj = NBDM_BuildingSegmentHeatingSystems()

    if pdf_hvac_data := _pdf_data.get_section(WufiPDF_HVAC):
        # --- Heat Pumps ------------------------------------------------------
        for pdf_heat_pump_device_data in pdf_hvac_data.heat_pump_devices:
            new_device = NBDM_HeatingDevice()
            new_device.device_type = heating_device_type.HEAT_PUMP
            new_device.display_name = pdf_heat_pump_device_data.device_name
            new_device.coverage_segment_heating = (
                pdf_heat_pump_device_data.coverage_heating
            )
            new_device.coverage_segment_cooling = (
                pdf_heat_pump_device_data.coverage_cooling
            )
            obj.add_device(new_device)

        # --- Electric Heaters ------------------------------------------------
        for pdf_elec_heating_device_data in pdf_hvac_data.electric_heating_devices:
            new_device = NBDM_HeatingDevice()
            new_device.device_type = heating_device_type.DIRECT_ELECTRIC
            new_device.display_name = pdf_elec_heating_device_data.device_name
            new_device.coverage_segment_heating = (
                pdf_elec_heating_device_data.coverage_heating
            )
            obj.add_device(new_device)

    return obj
