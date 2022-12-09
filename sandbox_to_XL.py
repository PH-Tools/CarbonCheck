# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Testing Excel Report Output."""

import pathlib

import xlwings as xw

from NBDM.to_JSON import write
from NBDM.from_JSON import read

from tests.conftest import sample_Project

# -- Read in a JSON, create a new NBDM from it
json_file = pathlib.Path("example.json")
write.NBDM_Project_to_json_file(sample_Project, json_file)
nbdm_project = read.NBDM_Project_from_json_file(json_file)

# # -- Write to Excel
from NBDM.to_Excel import report
from PHX.xl import xl_app

xl = xl_app.XLConnection(xl_framework=xw, output=print)
output_report = report.OutputReport(_xl=xl, _sheet_name="NBDM")
row_num = 1
with xl.in_silent_mode():
    row_num = output_report.write_NBDM_Project(nbdm_project, row_num)
    row_num = output_report.write_NBDM_WholeBuilding(nbdm_project, row_num)
    row_num = output_report.write_NBDM_BuildingSegments(nbdm_project, row_num)
    output_report.autofit_columns()
    output_report.hide_group_details()
