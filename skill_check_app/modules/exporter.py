import pdfkit
import os

def export_html_to_pdf(html_str: str, output_path: str) -> str:
    # Ensure wkhtmltopdf is installed and callable
    try:
        pdfkit.from_string(html_str, output_path)
        return output_path
    except Exception as e:
        return f"PDF Export Error: {str(e)}"
