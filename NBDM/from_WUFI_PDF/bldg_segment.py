# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM BuildingSegment objects from WUFI-PDF data."""

from typing import Dict
from NBDM.from_WUFI_PDF.geometry import build_NBDM_geometryFromWufiPDF
from NBDM.from_WUFI_PDF.occupancy import build_NBDM_occupancyFromWufiPDF
from NBDM.from_WUFI_PDF.performance import build_NBDM_performanceFromWufiPDF

from NBDM.model import building
from NBDM.model import enums

from NBDM.from_WUFI_PDF.pdf_sections.typing import PDFSectionType


def create_NBDM_BuildingSegmentFromWufiPDF(
    _pdf_data: Dict[str, PDFSectionType]
) -> building.NBDM_BuildingSegment:
    """Read in data from a PHPP and build up a new BuildingSegment."""

    return building.NBDM_BuildingSegment(
        segment_name="- - WUFI-PDF File Name - -",
        construction_type=enums.construction_type.NEW_CONSTRUCTION,
        construction_method=enums.construction_method.METHOD_A,
        geometry=build_NBDM_geometryFromWufiPDF(_pdf_data),
        occupancy=build_NBDM_occupancyFromWufiPDF(_pdf_data),
        performance=build_NBDM_performanceFromWufiPDF(_pdf_data),
    )
