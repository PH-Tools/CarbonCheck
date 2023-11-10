# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM_BuildingSegmentOccupancy objects from WUFI-PDF data."""

from typing import Dict

from NBDM.model import occupancy
from NBDM.from_WUFI_PDF.pdf_sections.__typing import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.bldg_info import WufiPDF_BuildingInformation


def build_NBDM_occupancyFromWufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType]
) -> occupancy.NBDM_BuildingSegmentOccupancy:
    bldg_info: WufiPDF_BuildingInformation = _pdf_data[WufiPDF_BuildingInformation.__pdf_heading_string__]  # type: ignore
    return occupancy.NBDM_BuildingSegmentOccupancy(
        total_dwelling_units=bldg_info.units,
        total_occupants=bldg_info.number_of_occupants,
    )
