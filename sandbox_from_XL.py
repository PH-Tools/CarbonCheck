# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Testing PHPP Input."""

import xlwings as xw

# # -- Read in from Excel
from PHX.xl import xl_app
from PHX.PHPP import phpp_app

if __name__ == "__main__":
    xl = xl_app.XLConnection(xl_framework=xw, output=print)
    phpp_conn = phpp_app.PHPPConnection(xl)

    try:
        xl.output(f"> connected to excel doc: {phpp_conn.xl.wb.name}")
    except xl_app.NoActiveExcelRunningError as e:
        raise e

    site_energy = phpp_conn.per.get_site_energy_by_fuel_type()

    for k, v in site_energy.items():
        print(k, "-" * 25)
        print(v)
