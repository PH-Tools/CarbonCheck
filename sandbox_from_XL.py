# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Testing PHPP Input."""

import xlwings as xw
from rich import print

from PHX.xl import xl_app
from PHX.PHPP import phpp_app

from NBDM.from_PHPP import create_building


if __name__ == "__main__":
    # -- Connect to Excel
    xl = xl_app.XLConnection(xl_framework=xw, output=print)
    phpp_conn = phpp_app.PHPPConnection(xl)

    with phpp_conn.xl.in_silent_mode():
        bldg = create_building.create_NBDM_Building(phpp_conn)
        print(bldg)

        # building = project.NBDM_Building()

        # proposed_variant = project.NBDM_Variant(name="", building="")
        # baseline_variant = project.NBDM_Variant(name="", building="")

        # project.NBDM_Variants(proposed_variant, baseline_variant)

        # project.NBDM_Project
        #     team,
        #     site,
        #     variants,
        # )
