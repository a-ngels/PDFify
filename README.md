# PDFify

Automate filling HIPAA PDF forms with patient data from Excel.

## Features
- Reads patient details from an Excel file (`patients.xlsx`).
- Fills a HIPAA authorization PDF (`hipaa_fillable.pdf`) with the data.
- Supports text fields and checkboxes.
- Outputs one PDF per patient.

## Requirements
- Python 3.10+
- [pandas](https://pandas.pydata.org/)
- [PyPDF2](https://pypdf2.readthedocs.io/)

Install dependencies:
```bash
pip install pandas PyPDF2
