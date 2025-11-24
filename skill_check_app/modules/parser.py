import io
import docx
import PyPDF2


# ======================================================
# Extract text from PDF
# ======================================================
def extract_text_from_pdf(file) -> str:
    """
    Extract text from PDF using PyPDF2.
    """
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
        return text.strip()
    except Exception:
        return ""


# ======================================================
# Extract text from DOCX
# ======================================================
def extract_text_from_docx(file) -> str:
    """
    Extract text from DOCX using python-docx.
    """
    try:
        doc = docx.Document(file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text.strip()
    except Exception:
        return ""


# ======================================================
# Extract text from TXT
# ======================================================
def extract_text_from_txt(file) -> str:
    """
    Reads plain text files.
    """
    try:
        return file.read().decode("utf-8", errors="ignore")
    except Exception:
        try:
            # fallback
            return file.read().decode(errors="ignore")
        except:
            return ""


# ======================================================
# Resume parser wrapper
# ======================================================
def parse_resume(file) -> str:
    """
    Accepts PDF / DOCX / TXT and returns plain text resume.
    """
    if file is None:
        return ""

    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file)

    if filename.endswith(".txt"):
        return extract_text_from_txt(file)

    return ""


# ======================================================
# JD parser wrapper
# (same as resume parser but separated for clarity)
# ======================================================
def parse_jd(file) -> str:
    if file is None:
        return ""

    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file)

    if filename.endswith(".txt"):
        return extract_text_from_txt(file)

    return ""
# ======================================================