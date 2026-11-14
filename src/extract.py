import json
import sys
from typing import Optional

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ValidationError
from read_pdf import read_pdf_text
from validate import check_totals

from read_pdf import read_pdf_text

load_dotenv(override=True)
client = Groq()  
MODEL = "openai/gpt-oss-20b"  


class Invoice(BaseModel):
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    tax: Optional[float] = None
    delivery: Optional[float] = None
    total: Optional[float] = None


PROMPT = """You extract fields from invoice text. Reply with JSON only, \
using exactly these keys: vendor, invoice_number, date, subtotal, discount, \
tax, delivery, total.

Rules:
- vendor: the business that issued the invoice (the seller), not the customer.
- invoice_number: the invoice, bill, or reference number exactly as printed.
- date: the invoice date as YYYY-MM-DD. Dates like 21/10/2026 are day/month/year.
- subtotal: the sum of the items before any discount, tax, or extra charges.
- discount: the discount amount as a positive number (a printed -1,050 becomes 1050).
- tax: the total tax amount (not the rate).
- delivery: delivery, shipping, or other extra charges added to the bill.
- total: the final amount payable.
- All amounts are plain numbers: remove commas, currency symbols, and lakh-style \
grouping (1,35,700 becomes 135700).
- If a field is not printed on the invoice, use null. Do not guess, and do not \
calculate missing values yourself."""

def extract_invoice(text):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text},
        ],
    )
    raw = response.choices[0].message.content
    return Invoice.model_validate(json.loads(raw))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"--- {path}")
        try:
            invoice = extract_invoice(read_pdf_text(path))
            print(invoice.model_dump_json(indent=2))
            print("Check:", check_totals(invoice)["message"])
        except (ValidationError, json.JSONDecodeError) as err:
            print("Could not parse the model's answer:", err)