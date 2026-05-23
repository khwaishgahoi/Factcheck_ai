from docx import Document

def extract_text_from_docx(docx_file):

    doc = Document(docx_file)

    text = ""

    for para in doc.paragraphs:

        if para.text.strip():
            text += para.text + "\n"

    return text