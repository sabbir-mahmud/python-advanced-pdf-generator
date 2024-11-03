import datetime
import os
from tempfile import NamedTemporaryFile

import pdfkit
from jinja2 import Environment, FileSystemLoader


def generate_pdf_invoice():
    #  bulk data for generate invoice
    data = {
        "company": {
            "name": "One Islam",
            "street": "Vil-Kaliganj, Thana-Ullapara",
            "city": "Sirajganj",
            "st": "Rajshahi",
            "country": "Bangladesh",
            "zip": "6760",
            "phone": "+8801782844241",
            "fax": "000-000-0000",
            "website": "oneislam.pro",
        },
        "bill_to": {
            "name": "John Doe",
            "company": "Doe Enterprises",
            "street": "123 Main St",
            "city": "Anytown",
            "st": "CA",
            "zip": "12345",
            "phone": "555-555-5555",
        },
        "invoice": {
            "date": "12/9/2019",
            "number": "123456",
            "customer_id": "123",
            "due_date": "1/8/2020",
        },
        "invoice_items": [
            {"description": "Service Fee", "taxed": "", "amount": 230.00},
            {"description": "Labor: 5 hours at $75/hr", "taxed": "", "amount": 375.00},
            {"description": "Parts", "taxed": "X", "amount": 345.00},
        ],
        "comments": [
            "Total payment due in 30 days",
            "Please include the invoice number on your check",
        ],
        "totals": {
            "subtotal": 950.00,
            "taxable": 345.00,
            "tax_rate": 6.25,
            "tax_due": 21.56,
            "other": 0.00,
            "total": 971.56,
        },
        "payment_info": {"payable_to": "Your Company Name"},
        "contact_info": {
            "contact_name": "John Doe",
            "contact_phone": "555-555-5555",
            "contact_email": "john.doe@example.com",
        },
    }

    # process html with jinja
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    html_content = template.render(data=data).encode("utf-8")

    # wkhtmltopdf configurations
    path_to_wkhtmltopdf = "/usr/local/bin/wkhtmltopdf"  # Adjust if needed
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    options = {}

    # saving output
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"invoice_{timestamp}.pdf")

    with NamedTemporaryFile(delete=True) as temp_file:
        pdfkit.from_string(
            html_content.decode("utf-8"),
            output_path,
            configuration=config,
            options=options,
        )

    print(f"PDF invoice generated and saved at {output_path}")
    return output_path


if __name__ == "__main__":
    # calling generate invoice function
    generate_pdf_invoice()
