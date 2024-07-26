import pytesseract
from PIL import Image

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR'


def jpg_to_txt(img_filename):
    try:
        return pytesseract.image_to_string(Image.open(img_filename))
    except:
        return ''


def png_to_txt(img_filename):
    # will replace transparent pixels with white
    try:
        image = Image.open(img_filename)
        augmented = Image.composite(image, Image.new('RGB', image.size, 'white'), image)
        return pytesseract.image_to_string(augmented)
    except:
        return ''


def pillow_to_txt(pil_img):
    try:
        return pytesseract.image_to_string(pil_img)
    except:
        return ''
