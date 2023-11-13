from NBDM.from_WUFI_PDF.pdf_reader import PDFReader


def test_multiple_readers_are_independent() -> None:
    reader_1 = PDFReader()
    reader_2 = PDFReader()

    assert id(reader_1) != id(reader_2)
    assert id(reader_1.pdf_sections) != id(reader_2.pdf_section_classes)
