to compile, run the following:
pyuic6 -o ./App/views/ui_files/layout_app.py ./App/views/ui_files/layout_app.ui



# -- Usage:
usage: pyuic6 [-h] [-V] [-p] [-o FILE] [-x] [-d] [-i N] ui

Python User Interface Compiler

positional arguments:
  ui                    the .ui file created by Qt Designer

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -p, --preview         show a preview of the UI instead of generating code
  -o FILE, --output FILE
                        write generated code to FILE instead of stdout
  -x, --execute         generate extra code to test and display the class
  -d, --debug           show debug output
  -i N, --indent N      set indent width to N spaces, tab if N is 0 [default: 4]

