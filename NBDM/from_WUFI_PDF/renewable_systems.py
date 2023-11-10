# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Renewable Energy Systems from WUFI-PDF."""

from typing import Dict

from ph_units.unit_type import Unit

from NBDM.model.renewable_systems import (
    NBDM_BuildingSegmentRenewableSystems,
    NBDM_SolarDHWDevice,
    NBDM_SolarPVDevice,
)
from NBDM.from_WUFI_PDF.pdf_reader import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC


def create_NBDM_Renewable_Systems_from_WufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType],
) -> NBDM_BuildingSegmentRenewableSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentRenewableSystems Object."""
    obj = NBDM_BuildingSegmentRenewableSystems()

    pdf_hvac_data: WufiPDF_HVAC
    if pdf_hvac_data := _pdf_data[WufiPDF_HVAC.__pdf_heading_string__]:
        for pdf_renewable_device_data in pdf_hvac_data.renewable_devices:
            new_vent_unit = NBDM_SolarPVDevice(
                display_name=pdf_renewable_device_data.device_name,
                footprint=Unit(0.0, "FT2"),
                size=Unit(0.0, "KW"),
                annual_pv_energy=pdf_renewable_device_data.annual_energy_production,
            )
            obj.add_solar_pv_device(new_vent_unit)

    return obj
