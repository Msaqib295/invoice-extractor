# Invoice Extractor

A tool that reads invoices (PDF or photo), extracts key fields with an LLM, and lets a person review, correct, and export them to CSV.

**Status:** Early development (Phase 1: Added a script src/read_pdf.py that opens pdfs and prints its data in terminal).

## Planned flow
1. Upload an invoice
2. Extract vendor, invoice number, date, total, and tax
3. Check that the numbers add up
4. Review and correct in a side-by-side screen
5. Export to CSV
6. Create a python script by importing sys and pdfplumber
7. Script reads a pdf and prints its data in terminal

## Tech stack (planned)
Flutter (for both app and web) · FastAPI · Groq LLM · Pydantic · pdfplumber + Tesseract OCR

## Sample data
All invoices in `samples/` are synthetic (fictional businesses and made-up figures). Results on real-world documents may differ, since real invoices are usually messier.

## Answer key (`answers.csv`)
Correct values for each sample invoice, used to measure extraction accuracy.
- `split`: `build` (used while developing) or `test` (held out for evaluation)
- `date`: always `YYYY-MM-DD`
- `total`, `tax`: plain numbers, no commas or currency symbols; `tax` is the tax amount, not the rate
- Blank cell = field not present on the invoice

## Roadmap
- [x] Phase 0: Sample invoices and answer key
- [x] Phase 1: Extraction script
- [ ] Phase 2: Accuracy check and number validation
- [ ] Phase 3: FastAPI backend
- [ ] Phase 4: Flutter web/app
- [ ] Phase 5: Deployment
- [ ] Phase 6: Demo and write-up
