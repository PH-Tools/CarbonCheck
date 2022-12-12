# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Testing PHPP Input."""

import xlwings as xw
from rich import print

# # -- Read in from Excel
from NBDM.from_PHPP import build_performance
from PHX.xl import xl_app
from PHX.PHPP import phpp_app

if __name__ == "__main__":
    # -- Connect to Excel
    xl = xl_app.XLConnection(xl_framework=xw, output=print)
    phpp_conn = phpp_app.PHPPConnection(xl)

    with phpp_conn.xl.in_silent_mode():
        perf = build_performance.build_NBDM_performance(phpp_conn)
        print(perf)
