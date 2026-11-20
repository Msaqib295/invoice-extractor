# Invoice Extractor

A tool that reads invoices (PDF or photo), extracts key fields with an LLM, and lets a person review, correct, and export them to CSV.

**Status:** Phase 1 complete. A command-line script extracts fields from PDF invoices. Accuracy testing, the API, and the web app are still to come.

## Planned flow
1. Upload an invoice
2. Extract vendor, invoice number, date, total, and tax
3. Check that the numbers add up
4. Review and correct in a side-by-side screen
5. Export to CSV

## How it works today
`src/read_document.py` reads digital PDFs directly, and runs OCR (Tesseract) on photos and scanned PDFs, keeping each word's position for highlighting later. `src/extract.py` sends the text to an LLM (Groq) with strict instructions and validates the reply with Pydantic. `src/validate.py` checks that subtotal, discount, tax, and delivery add up to the total, and `src/evaluate.py` scores results against `answers.csv`.

## Run it
1. Clone the repo and create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # macOS / Linux
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your own Groq API key.
3. Run the extractor on one or more PDFs:
   ```
   python src/extract.py samples/inv01.pdf samples/inv02.pdf samples/inv03.pdf
   ```

## Sample data
All invoices in `samples/` are synthetic (fictional businesses and made-up figures). They are cleaner than real-world documents, so results on real invoices may differ.

## Answer key (`answers.csv`)
Correct values for each sample invoice, used to measure extraction accuracy.
- `split`: `build` (used while developing) or `test` (held out for evaluation)
- `vendor`: the seller's name as printed (compared ignoring capitalization)
- `date`: always `YYYY-MM-DD`
- `total`, `tax`: plain numbers, no commas or currency symbols; `tax` is the tax amount, not the rate
- Blank cell = field not present on the invoice

## Results
Prompt v2 (8 fields: vendor, invoice number, date, subtotal, discount, tax, delivery, total), Groq `openai/gpt-oss-20b`.

| Set | Invoices | Fields correct | Number check |
|---|---|---|---|
| Build | 5 | 40 / 40 | 5 ok |
| Test (held out) | 3 digital PDFs | 24 / 24 | 3 ok |

Earlier prompt v1 (5 fields) scored 25 / 25 on the build set.

**Limitations:** all invoices are synthetic and clean. The two phone-photo invoices are not yet scored because OCR is not implemented. A small test set means a perfect score says little about real-world documents.

## Tech stack
Python · pdfplumber · Groq LLM · Pydantic
Planned: FastAPI · Flutter (web) · Tesseract OCR · Cloud Run

## Roadmap
- [x] Phase 0: Sample invoices and answer key
- [x] Phase 1: Extraction script
- [ ] Phase 2: Accuracy check and number validation
- [ ] Phase 3: FastAPI backend
- [ ] Phase 4: Flutter web app
- [ ] Phase 5: Deployment
- [ ] Phase 6: Demo and write-up