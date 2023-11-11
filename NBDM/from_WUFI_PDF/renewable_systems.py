# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Renewable Energy Systems from WUFI-PDF."""


from ph_units.unit_type import Unit

from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC
from NBDM.model.renewable_systems import (
    NBDM_BuildingSegmentRenewableSystems,
    NBDM_SolarPVDevice,
)


def create_NBDM_Renewable_Systems_from_WufiPDF(
    _pdf_data: PDFSectionsCollection,
) -> NBDM_BuildingSegmentRenewableSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentRenewableSystems Object."""
    obj = NBDM_BuildingSegmentRenewableSystems()

    if pdf_hvac_data := _pdf_data.get_section(WufiPDF_HVAC):
        for pdf_renewable_device_data in pdf_hvac_data.renewable_devices:
            new_vent_unit = NBDM_SolarPVDevice(
                display_name=pdf_renewable_device_data.device_name,
                footprint=Unit(0.0, "FT2"),
                size=Unit(0.0, "KW"),
                annual_pv_energy=pdf_renewable_device_data.annual_energy_production,
            )
            obj.add_solar_pv_device(new_vent_unit)

    return obj
