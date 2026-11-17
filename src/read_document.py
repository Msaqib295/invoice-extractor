import shutil
import sys
from pathlib import Path
import pymupdf
import pdfplumber
import pytesseract
from PIL import Image, ImageOps

if not shutil.which("tesseract"):
    default = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if Path(default).exists():
        pytesseract.pytesseract.tesseract_cmd = default

IMAGE_TYPES = {".jpg", ".jpeg", ".png"}
MIN_PDF_CHARS = 30  


MIN_WIDTH = 1600  # enlarge small images so Tesseract can read the characters


def ocr_image(img, page, psm=6):
    img = ImageOps.grayscale(img)
    if img.width < MIN_WIDTH:
        scale = MIN_WIDTH / img.width
        img = img.resize((MIN_WIDTH, int(img.height * scale)), Image.LANCZOS)
    img = ImageOps.autocontrast(img)
    config = f"--psm {psm}" if psm else ""
    text = pytesseract.image_to_string(img, config=config)
    data = pytesseract.image_to_data(img, config=config, output_type=pytesseract.Output.DICT)
    words = [
        {"text": t, "page": page, "x": data["left"][i], "y": data["top"][i],
         "w": data["width"][i], "h": data["height"][i]}
        for i, t in enumerate(data["text"]) if t.strip()
    ]
    return text, words


def read_document(path):
    if Path(path).suffix.lower() in IMAGE_TYPES:
        img = ImageOps.exif_transpose(Image.open(path))  # fix phone rotation flag
        return ocr_image(img, page=1)

    texts, words = [], []
    with pdfplumber.open(path) as pdf:
        for n, page in enumerate(pdf.pages, start=1):
            texts.append(page.extract_text() or "")
            for w in page.extract_words():
                words.append({"text": w["text"], "page": n, "x": w["x0"], "y": w["top"],
                              "w": w["x1"] - w["x0"], "h": w["bottom"] - w["top"]})
    text = "\n".join(texts)
    if len(text.strip()) >= MIN_PDF_CHARS:
        return text, words

    # scanned PDF: render each page to an image, then OCR it
    texts, words = [], []
    for n, page in enumerate(pymupdf.open(path), start=1):
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        t, w = ocr_image(img, n)
        texts.append(t)
        words.extend(w)
    return "\n".join(texts), words


if __name__ == "__main__":
    print(read_document(sys.argv[1])[0])