import sys
import pdfplumber


def read_pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


if __name__ == "__main__":
    print(read_pdf_text(sys.argv[1]))
