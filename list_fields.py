from PyPDF2 import PdfReader

reader = PdfReader("hipaa_fillable.pdf")
fields = reader.get_fields()

for field_name, field_info in fields.items():
   print(f"{field_name}: {field_info}")