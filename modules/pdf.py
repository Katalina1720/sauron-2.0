from io import BytesIO

from PIL import Image
from PyPDF2 import PdfReader

from modules.img_plugin import pillow_to_txt


def read_file(pdf_path: str) -> str:
    pdf_text = []
    for page in PdfReader(pdf_path).pages:
        pdf_text.append(page.extract_text())
        for image in page.images:
            text = pillow_to_txt(Image.open(BytesIO(bytes(image.data))))
            pdf_text.append(text)
    return "".join(pdf_text)
