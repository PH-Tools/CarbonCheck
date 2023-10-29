# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create NBDM Envelope from WUFI-PDF."""

from typing import List


from NBDM.model.envelope import (
    NBDM_BuildingSegmentEnvelope,
    NBDM_AssemblyType,
    NBDM_GlazingType,
)


def create_NBDM_Envelope_from_WufiPDF(_pdf_data) -> NBDM_BuildingSegmentEnvelope:
    new_obj = NBDM_BuildingSegmentEnvelope()

    return new_obj
