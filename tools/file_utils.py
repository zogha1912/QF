from pdf2image import convert_from_path
import pytesseract
import os
from tempfile import NamedTemporaryFile
from typing import List


from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

def extract_text_from_pdf_ocr(file_bytes: bytes) -> str:
    images = convert_from_bytes(file_bytes)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf_ocr_(pdf_path: str) -> str:
    images = convert_from_path(pdf_path)
    full_text = ""
    for img in images:
        text = pytesseract.image_to_string(img)
        full_text += text + "\n"
    return full_text 

def extract_texts_from_multiple_pdfs(files: List[bytes]) -> List[str]:
    texts = []
    for file_bytes in files:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        text = extract_text_from_pdf_ocr_(tmp_path)
        texts.append(text)

        os.remove(tmp_path)
    return texts
