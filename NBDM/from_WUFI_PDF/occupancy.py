# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM_BuildingSegmentOccupancy objects from WUFI-PDF data."""


from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.bldg_info import WufiPDF_BuildingInformation
from NBDM.model import occupancy


def build_NBDM_occupancyFromWufiPDF(
    _pdf_data: PDFSectionsCollection,
) -> occupancy.NBDM_BuildingSegmentOccupancy:
    new_obj = occupancy.NBDM_BuildingSegmentOccupancy()
    if bldg_info := _pdf_data.get_section(WufiPDF_BuildingInformation):
        new_obj.total_dwelling_units = bldg_info.units
        new_obj.total_occupants = bldg_info.number_of_occupants
    return new_obj
