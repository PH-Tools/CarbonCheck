from rich import print
from pathlib import Path
from NBDM.from_WUFI_PDF.pdf_reader import PDFReader
from NBDM.from_WUFI_PDF.site import create_NBDM_Site_from_WufiPDF
from NBDM.from_WUFI_PDF.team import create_NBDM_Team_from_WufiPDF

reader = PDFReader()
reader.import_pdf_section_classes()
data = reader.extract_pdf_text(
    Path(
        "/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/01_Reference/_example_files/example_wufi_report.pdf"
    )
)

site = create_NBDM_Site_from_WufiPDF(data)
team = create_NBDM_Team_from_WufiPDF(data)
print(team)
