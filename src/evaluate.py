import csv
import sys

from extract import extract_invoice
from read_pdf import read_pdf_text

FIELDS = ["vendor", "invoice_number", "date", "total", "tax"]


def norm(field, value):
    if value is None or value == "":
        return None
    if field in ("total", "tax"):
        return round(float(value), 2)
    if field == "vendor":
        return " ".join(str(value).split()).lower()
    return str(value).strip()


def evaluate(split):
    with open("answers.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)
                if r["split"] == split and r["filename"].endswith(".pdf")]
    correct = total = 0
    for row in rows:
        try:
            got = extract_invoice(read_pdf_text("samples/" + row["filename"])).model_dump()
        except Exception as err:
            print(f"{row['filename']}: FAILED ({err})")
            got = {}
        for field in FIELDS:
            expected, actual = norm(field, row[field]), norm(field, got.get(field))
            total += 1
            if expected == actual:
                correct += 1
            else:
                print(f"{row['filename']} {field}: expected {expected!r}, got {actual!r}")
    print(f"\n{split}: {correct} of {total} fields correct")


if __name__ == "__main__":
    split = sys.argv[1] if len(sys.argv) > 1 else "build"
    if split == "test":
        print("Running the TEST set. Don't tune the prompt based on this.\n")
    evaluate(split)