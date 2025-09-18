import json
import os
import pdfkit
from jinja2 import Environment, FileSystemLoader

def render_certificate_to_pdf(cert_path, wkhtmltopdf_path):
    # 🔹 Validate certificate path
    if not os.path.exists(cert_path):
        raise FileNotFoundError(f"❌ Certificate file not found: {cert_path}")

    # 🔹 Load certificate data
    with open(cert_path, "r") as f:
        cert_data = json.load(f)

    # 🔹 Set up Jinja2 environment
    template_dir = "templates"
    template_file = "certificate_template.html"
    template_path = os.path.join(template_dir, template_file)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"❌ Template file not found: {template_path}")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    # 🔹 Render HTML from certificate data
    html_out = template.render(**cert_data)

    # 🔹 Validate wkhtmltopdf binary
    if not os.path.exists(wkhtmltopdf_path):
        raise FileNotFoundError(f"❌ wkhtmltopdf binary not found at: {wkhtmltopdf_path}")

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    # 🔹 Generate PDF filename
    cert_id = cert_data.get("certificate_id", "output")
    output_path = f"certificates/{cert_id}.pdf"

    # 🔹 PDF options to allow local image access
    options = {
        'enable-local-file-access': ''
    }

    # 🔹 Generate PDF
    pdfkit.from_string(html_out, output_path, configuration=config, options=options)
    print(f"✅ PDF certificate generated as '{output_path}'")
