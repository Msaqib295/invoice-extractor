import csv
import sys

from extract import extract_invoice
from read_pdf import read_pdf_text
from validate import check_totals

FIELDS = ["vendor", "invoice_number", "date", "subtotal",
          "discount", "tax", "delivery", "total"]
NUMERIC = {"subtotal", "discount", "tax", "delivery", "total"}


def norm(field, value):
    if value is None or value == "":
        return None
    if field in NUMERIC:
        return round(float(value), 2)
    if field == "vendor":
        return " ".join(str(value).split()).lower()
    return str(value).strip()


def evaluate(split):
    with open("answers.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)
                if r["split"] == split and r["filename"].endswith(".pdf")]
    correct = total = 0
    checks = {}
    for row in rows:
        got = {}
        try:
            invoice = extract_invoice(read_pdf_text("samples/" + row["filename"]))
            got = invoice.model_dump()
            status = check_totals(invoice)["status"]
        except Exception as err:
            print(f"{row['filename']}: FAILED ({err})")
            status = "failed"
        checks[status] = checks.get(status, 0) + 1
        for field in FIELDS:
            expected, actual = norm(field, row[field]), norm(field, got.get(field))
            total += 1
            if expected == actual:
                correct += 1
            else:
                print(f"{row['filename']} {field}: expected {expected!r}, got {actual!r}")
    print(f"\n{split}: {correct} of {total} fields correct")
    print("Number check results:", checks)


if __name__ == "__main__":
    split = sys.argv[1] if len(sys.argv) > 1 else "build"
    if split == "test":
        print("Running the TEST set. Don't tune the prompt based on this.\n")
    evaluate(split)