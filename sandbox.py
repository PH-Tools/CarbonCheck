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
from NBDM.to_Excel import xl_app

xl = xl_app.XLConnection(xl_framework=xw, output=print)
output_report = report.OutputReport(_xl=xl)
output_report.write_NBDM_Project(nbdm_project)
