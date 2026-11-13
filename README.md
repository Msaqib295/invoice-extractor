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
`src/read_pdf.py` pulls the text out of a PDF. `src/extract.py` sends that text to an LLM (Groq) with strict instructions, then validates the reply with Pydantic so malformed output fails loudly instead of silently.

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

## Early results
On the three clean synthetic invoices used while building, all five fields were extracted correctly. This is not an accuracy figure: those invoices are in the build set, and the held-out test set (including phone photos and a missing-field case) has not been created yet.

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