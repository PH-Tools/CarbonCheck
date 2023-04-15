# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Testing PHPP Input."""

import xlwings as xw
from rich import print

from PHX.xl import xl_app
from PHX.PHPP import phpp_app

from NBDM.model.project import NBDM_Project
from NBDM.from_PHPP import create_NBDM_BuildingSegment, create_NBDM_Team, create_NBDM_Site

if __name__ == "__main__":
    # -- Connect to Excel
    xl = xl_app.XLConnection(xl_framework=xw, output=print)
    phpp_conn = phpp_app.PHPPConnection(xl)

    new_proj = NBDM_Project()

    with phpp_conn.xl.in_silent_mode():
        new_proj.team = create_NBDM_Team(phpp_conn)
        new_proj.site = create_NBDM_Site(phpp_conn)
        # bldg_seg_a = create_NBDM_BuildingSegment(phpp_conn)

    # new_proj.variants.proposed.add_building_segment(bldg_seg_a)
    # new_proj.variants.baseline.add_building_segment(bldg_seg_a)
