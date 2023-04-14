# -*- Python Version: 3.10 -*-

"""Run to see GUI."""

import sys
import pathlib

from NBDM.model import output_format
from App.cc_app import CCApp


if __name__ == "__main__":
    app = CCApp(output_format, sys.argv)
    app.view.show()
    app.load_cc_project_from_file(pathlib.Path("example.json"))
    sys.exit(app.exec())
