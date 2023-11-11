from typing import Dict
from NBDM.from_WUFI_PDF.pdf_sections.__typing import SupportsWufiPDF_Section
from NBDM.from_WUFI_PDF.pdf_sections import annual_demand


def test_read_in_valid_pdf_file(
    sample_pdf_data_ridgeway_proposed: Dict[str, SupportsWufiPDF_Section]
) -> None:
    assert sample_pdf_data_ridgeway_proposed
