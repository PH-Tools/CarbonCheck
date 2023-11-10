# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM BuildingSegment objects from WUFI-PDF data."""

from typing import Dict

from NBDM.model import geometry
from NBDM.from_WUFI_PDF.pdf_sections.__typing import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.bldg_info import WufiPDF_BuildingInformation


def build_NBDM_geometryFromWufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType]
) -> geometry.NBDM_BuildingSegmentGeometry:
    new_geometry = geometry.NBDM_BuildingSegmentGeometry()

    # -- Pull out the data from the PDF dict, if it exists.
    bldg_info: WufiPDF_BuildingInformation
    if bldg_info := _pdf_data.get(WufiPDF_BuildingInformation.__pdf_heading_string__, None):  # type: ignore
        new_geometry.area_envelope = bldg_info.total_area_envelope
        new_geometry.area_floor_area_net_interior_weighted = bldg_info.floor_area
        new_geometry.volume_net_interior = bldg_info.enclosed_volume

    return new_geometry
