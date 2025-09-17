import json
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os

# 🔹 Load signed certificate
cert_path = "certificates/e842a1e7-f2ce-4640-8287-13f336dd4166.json"
if not os.path.exists(cert_path):
    raise FileNotFoundError(f"❌ Certificate file not found: {cert_path}")

with open(cert_path, "r") as f:
    cert_data = json.load(f)

# 🔹 Set up Jinja2 environment
template_dir = "templates"
template_file = "certificate_template.html"
env = Environment(loader=FileSystemLoader(template_dir))

if not os.path.exists(os.path.join(template_dir, template_file)):
    raise FileNotFoundError(f"❌ Template file not found: {template_file}")

template = env.get_template(template_file)

# 🔹 Render HTML with unpacked certificate data
html_out = template.render(**cert_data)

# 🔹 Specify path to wkhtmltopdf binary
path_to_wkhtmltopdf = r"C:\Users\KIIT\ZeroTrace_Cert\wkhtmltopdf\bin\wkhtmltopdf.exe"
if not os.path.exists(path_to_wkhtmltopdf):
    raise FileNotFoundError(f"❌ wkhtmltopdf binary not found at: {path_to_wkhtmltopdf}")

config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# 🔹 Generate PDF
output_path = "certificates/your_cert.pdf"
pdfkit.from_string(html_out, output_path, configuration=config)

print(f"✅ PDF certificate generated as '{output_path}'")
