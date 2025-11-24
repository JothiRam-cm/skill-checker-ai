# import pdfkit
# import os

# def export_html_to_pdf(html_str: str, output_path: str) -> str:
#     # Ensure wkhtmltopdf is installed and callable
#     try:
#         pdfkit.from_string(html_str, output_path)
#         return output_path
#     except Exception as e:
#         return f"PDF Export Error: {str(e)}"


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup

def export_html_to_pdf(html_str: str, output_path: str) -> str:
    """
    Convert simplified HTML text into PDF using ReportLab.
    Streamlit Cloud safe (no wkhtmltopdf).
    """

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    y = height - 50  # starting position
    line_height = 14

    soup = BeautifulSoup(html_str, "html.parser")
    text = soup.get_text()

    for line in text.split("\n"):
        if y <= 50:  # new page
            c.showPage()
            y = height - 50
        c.drawString(50, y, line.strip())
        y -= line_height

    c.save()
    return output_path
