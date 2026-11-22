import csv
import sys
from groq import APIConnectionError
from extract import extract_invoice
from read_document import read_document
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
        rows = [r for r in csv.DictReader(f) if r["split"] == split]
    correct = total = 0
    checks = {}
    for row in rows:
        got = {}
        try:
            text = read_document("samples/" + row["filename"])[0]
            invoice = extract_invoice(text)
            got = invoice.model_dump()
            status = check_totals(invoice)["status"]
            if "--show" in sys.argv:
                print(row["filename"], got)
        except APIConnectionError:
            sys.exit("Could not reach Groq. Check your internet and try again. No score computed.")
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
    if split.startswith("test"):
        print("Running the TEST set. Don't tune the prompt or OCR based on this.\n")
    evaluate(split)