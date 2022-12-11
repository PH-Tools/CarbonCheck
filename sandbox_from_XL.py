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
    print("- " * 25)
    xl = xl_app.XLConnection(xl_framework=xw, output=None)
    phpp_conn = phpp_app.PHPPConnection(xl)

    try:
        xl.output(f"> connected to excel doc: {phpp_conn.xl.wb.name}")
    except xl_app.NoActiveExcelRunningError as e:
        raise e

    with phpp_conn.xl.in_silent_mode():

        peak_heat_load = build_performance.build_peak_head_load(
            phpp_conn.heating_load.get_load_W1(), phpp_conn.heating_load.get_load_W2()
        )
        peak_cooling_load = build_performance.build_peak_cooling_load(
            phpp_conn.cooling_load.get_load_W1(), phpp_conn.cooling_load.get_load_W2()
        )
        print("- " * 25)
        print("peak_heat_load=", peak_heat_load)
        print("peak_cooling_load=", peak_cooling_load)

        annual_heating_demand = build_performance.build_annual_heating_demand(
            phpp_conn.heating.get_demand_kWh_year()
        )
        annual_cooling_demand = build_performance.build_annual_cooling_demand(
            phpp_conn.cooling.get_demand_kWh_year()
        )
        print("- " * 25)
        print("annual_heating_demand=", annual_heating_demand)
        print("annual_cooling_demand=", annual_cooling_demand)

        site_energy = build_performance.build_site_energy(
            phpp_conn.per.get_site_energy_by_fuel_type()
        )
        print("- " * 25)
        print("site_energy=", site_energy)
