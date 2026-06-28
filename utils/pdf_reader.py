import fitz


def extract_pdf_text(pdf_path):
    """
    Extract all text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text