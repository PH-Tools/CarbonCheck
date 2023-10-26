# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM_BuildingSegmentOccupancy objects from WUFI-PDF data."""

from typing import Dict

from NBDM.model import occupancy
from NBDM.from_WUFI_PDF.pdf_sections.typing import PDFSectionType
from NBDM.from_WUFI_PDF.pdf_sections.bldg_info import BuildingInformation


def build_NBDM_occupancyFromWufiPDF(
    _pdf_data: Dict[str, PDFSectionType]
) -> occupancy.NBDM_BuildingSegmentOccupancy:
    bldg_info: BuildingInformation = _pdf_data[BuildingInformation.__pdf_heading_string__]  # type: ignore
    return occupancy.NBDM_BuildingSegmentOccupancy(
        total_dwelling_units=bldg_info.units,
        total_occupants=bldg_info.number_of_occupants,
    )
