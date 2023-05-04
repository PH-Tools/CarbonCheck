# -*- Python Version: 3.10 -*-

"""Run to see GUI."""

import logging
import sys

try:
    from NBDM.model import output_format
except Exception as e:
    raise Exception("Error importing NBDM library?", e)

try:
    from App.cc_app import CCApp
except Exception as e:
    raise Exception("Error importing App library?", e)

if __name__ == "__main__":
    app = CCApp(output_format, sys.argv)
    app.view.show()
    sys.exit(app.exec())
