import pdfplumber
import docx

def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages)

def read_docx(file):
    doc = docx.Document(file)
    return " ".join([p.text for p in doc.paragraphs])

def read_txt(file):
    return file.read().decode("utf-8")

def process_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return read_pdf(uploaded_file)
    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        return read_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return read_txt(uploaded_file)
    else:
        return None
