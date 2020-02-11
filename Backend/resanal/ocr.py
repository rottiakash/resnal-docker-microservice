import pytesseract
from PIL import Image

def get_ocr(src):
    image = Image.open(src)
    text = pytesseract.image_to_string(image)
    return text