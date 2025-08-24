import docx
from PyPDF2 import PdfReader
import io

def parse_pdf(file_content: bytes) -> str:
    """
    Parses the content of a PDF file and extracts text.
    """
    try:
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

def parse_docx(file_content: bytes) -> str:
    """
    Parses the content of a DOCX file and extracts text.
    """
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return ""