import datetime
import os
from tempfile import NamedTemporaryFile

import pdfkit
from jinja2 import Environment, FileSystemLoader
from pytz import timezone as pytz_timezone


def generate_pdf_invoice():
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")

    # Generate date for the invoice
    date = datetime.datetime.now().astimezone(pytz_timezone("Etc/GMT+7")).date()

    # Render HTML content
    html_content = template.render().encode("utf-8")

    # Set up wkhtmltopdf configuration
    path_to_wkhtmltopdf = "/usr/bin/wkhtmltopdf"  # Adjust if needed
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    options = {}

    # Create 'output' folder if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"invoice_{timestamp}.pdf")

    # Save the PDF file
    with NamedTemporaryFile(delete=True) as temp_file:
        pdfkit.from_string(
            html_content.decode("utf-8"),
            output_path,
            configuration=config,
            options=options,
        )

    print(f"PDF invoice generated and saved at {output_path}")
    return output_path


generate_pdf_invoice()
