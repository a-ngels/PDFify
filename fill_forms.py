import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject

excel_file = "patients.xlsx"
pdf_template = "hipaa_fillable.pdf"

# helper function to format dates
def format_date(value):
   if pd.isna(value):
      return ""
   if isinstance(value, str):
      if value.strip().lower() == "present":
         return "present"
      return value.strip()
   if isinstance(value, (pd.Timestamp, )):
      return value.strftime("%m/%d/%Y")
   return str(value)

# load excel file
df_preview = pd.read_excel(excel_file, nrows=1)
if df_preview.columns[0] == "Table 1":
   df = pd.read_excel(excel_file, skiprows=1)
else:
   df = pd.read_excel(excel_file)

# clean col names and check required column
df.columns = df.columns.str.strip()
if "PatientName" in df.columns:
   df = df.dropna(subset=["PatientName"])
else:
   raise ValueError("'PatientName' column missing! Check your Excel file.")

# go through each row and fill the PDF form
for i, row in df.iterrows():
   reader = PdfReader(pdf_template)
   writer = PdfWriter()

   for page in reader.pages:
      writer.add_page(page)

   # set text fields
   data = {
      "Name": str(row.get("PatientName", "")),
      "Date": format_date(row.get("DOB")),
      "Address": str(row.get("PatientAddress", "")),
      "Provider Name": str(row.get("Provider", "")),
      "Receipient Name": str(row.get("Recipient", "")),
      "From Date": format_date(row.get("FromDate")),
      "To Date": format_date(row.get("ToDate")),
      "Other Text": str(row.get("Sec9_text", "")),     # Sec 9 text
      "Event": str(row.get("ExpireEvent", "")),
      "Other Name": str(row.get("SignerName", "")),
      "Authority": str(row.get("Authority", "")),
      "Other 2": str(row.get("Sec10_text", "")),       # Sec 10 text
   }

   # Apply text values
   writer.update_page_form_field_values(writer.pages[0], data)

   # --- Explicitly handle checkboxes ---
   for annot in writer.pages[0]["/Annots"]:
      obj = annot.get_object()
      field_name = obj.get("/T")

      # Section 9
      if field_name == "Med rec Date" and str(row.get("MedRecDate")).strip().lower() == "yes":
         obj.update({NameObject("/V"): NameObject("/Yes")})
         obj.update({NameObject("/AS"): NameObject("/Yes")})

      if field_name == "Entire Med Rec" and str(row.get("EntireMedRec")).strip().lower() == "yes":
         obj.update({NameObject("/V"): NameObject("/Yes")})
         obj.update({NameObject("/AS"): NameObject("/Yes")})

      if field_name == "Other" and str(row.get("Sec9_check")).strip().lower() == "yes":
         obj.update({NameObject("/V"): NameObject("/Yes")})
         obj.update({NameObject("/AS"): NameObject("/Yes")})

      # Section 10
      if field_name == "Request Of" and str(row.get("Sec10_check")).strip().lower() == "yes":
         obj.update({NameObject("/V"): NameObject("/Yes")})
         obj.update({NameObject("/AS"): NameObject("/Yes")})

   # save pdf
   patient_name = str(row.get("PatientName", "")).strip()
   output_file = f"{patient_name} HIPAA Form_{i+1}.pdf"
   with open(output_file, "wb") as out:
      writer.write(out)