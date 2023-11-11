# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM BuildingSegment objects from WUFI-PDF data."""


from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.bldg_info import WufiPDF_BuildingInformation
from NBDM.model import geometry


def build_NBDM_geometryFromWufiPDF(
    _pdf_data: PDFSectionsCollection,
) -> geometry.NBDM_BuildingSegmentGeometry:
    new_geometry = geometry.NBDM_BuildingSegmentGeometry()

    # -- Pull out the data from the PDF dict, if it exists.
    if bldg_info := _pdf_data.get_section(WufiPDF_BuildingInformation):
        new_geometry.area_envelope = bldg_info.total_area_envelope
        new_geometry.area_floor_area_net_interior_weighted = bldg_info.floor_area
        new_geometry.volume_net_interior = bldg_info.enclosed_volume

    return new_geometry
