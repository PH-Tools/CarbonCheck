from typing import Dict
from NBDM.from_WUFI_PDF.pdf_sections import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections import annual_demand


def test_read_in_valid_pdf_file(
    sample_pdf_data_ridgeway: Dict[str, WufiPDF_SectionType]
) -> None:
    assert sample_pdf_data_ridgeway
