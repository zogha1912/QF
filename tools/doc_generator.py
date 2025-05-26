from docx import Document
from docx.shared import Inches
import os

def create_attestation_docx(attestation_text, filename="attestation.docx"):
    doc = Document()
    doc.add_paragraph(attestation_text)
    doc.save(filename)
    return filename
