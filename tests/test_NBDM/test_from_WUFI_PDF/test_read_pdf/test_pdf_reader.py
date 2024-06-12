from NBDM.from_WUFI_PDF.pdf_reader import PDFReader
from NBDM.from_WUFI_PDF.pdf_sections.areas import WufiPDF_Areas


def test_multiple_readers_are_independent() -> None:
    reader_1 = PDFReader()
    reader_2 = PDFReader()

    assert reader_1 != reader_2
    assert id(reader_1) != id(reader_2)
    assert reader_1.pdf_sections != reader_2.pdf_section_classes
    assert id(reader_1.pdf_sections) != id(reader_2.pdf_section_classes)

    assert reader_1.pdf_sections != reader_2.pdf_sections
    assert id(reader_1.pdf_sections) != id(reader_2.pdf_sections)

    assert reader_1.pdf_sections.get_section(
        WufiPDF_Areas
    ) != reader_2.pdf_sections.get_section(WufiPDF_Areas)
