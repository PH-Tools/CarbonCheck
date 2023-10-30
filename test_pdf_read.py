from rich import print
from pathlib import Path
from NBDM.from_WUFI_PDF.pdf_reader import PDFReader
from NBDM.from_WUFI_PDF import (
    create_NBDM_Envelope_from_WufiPDF,
    create_NBDM_Appliances_from_WufiPDF,
    create_NBDM_Heating_Systems_from_WufiPDF,
    create_NBDM_Cooling_Systems_from_WufiPDF,
    create_NBDM_Vent_Systems_from_WufiPDF,
    create_NBDM_DHW_Systems_from_WufiPDF,
    create_NBDM_Renewable_Systems_from_WufiPDF,
)

reader = PDFReader()
reader.import_pdf_section_classes()
# pdf_data = reader.extract_pdf_text(
#     Path(
#         "/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/01_Reference/_example_files/example_wufi_report.pdf"
#     )
# )
pdf_data = reader.extract_pdf_text(Path("/Users/em/Desktop/arverne_proposed.pdf"))

# heating_systems = create_NBDM_Heating_Systems_from_WufiPDF(pdf_data)
# cooling_systems = create_NBDM_Cooling_Systems_from_WufiPDF(pdf_data)
# ventilation_systems = create_NBDM_Vent_Systems_from_WufiPDF(pdf_data)
# dhw_systems = create_NBDM_DHW_Systems_from_WufiPDF(pdf_data)
# renewable_systems = create_NBDM_Renewable_Systems_from_WufiPDF(pdf_data)

# print(renewable_systems)
