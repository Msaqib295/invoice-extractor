import json
import sys
from typing import Optional

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ValidationError

from read_pdf import read_pdf_text

load_dotenv(override=True)
client = Groq()  # reads GROQ_API_KEY from the environment
MODEL = "openai/gpt-oss-20b"  # same model you used in Study Buddy


class Invoice(BaseModel):
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None


PROMPT = """You extract fields from invoice text. Reply with JSON only, \
using exactly these keys: vendor, invoice_number, date, total, tax.

Rules:
- vendor: the business that issued the invoice (the seller), not the customer.
- invoice_number: the invoice, bill, or reference number exactly as printed.
- date: the invoice date as YYYY-MM-DD. Dates like 21/10/2026 are day/month/year.
- total: the final amount payable, as a plain number (no commas, no currency symbol).
- tax: the total tax amount (not the rate), as a plain number.
- If a field is not on the invoice, use null. Do not guess."""


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
            print(extract_invoice(read_pdf_text(path)).model_dump_json(indent=2))
        except (ValidationError, json.JSONDecodeError) as err:
            print("Could not parse the model's answer:", err)