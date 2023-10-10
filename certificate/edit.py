import PyPDF2
import time

from fpdf import FPDF


def edit_cert(address):
    old_text = "______"
    pdf_file = PyPDF2.PdfReader(open("certificate/start.pdf", "rb"))
    page = pdf_file.pages[0]
    text = page.extract_text()
    str = f"{address}\n\nЗадолженность отсутствует."
    text = text.replace(old_text, str)
    print(text)
    return create_new_cert(text, address)


def create_new_cert(text, adr):
    pdf = FPDF()
    text2 = text.encode("utf-8").decode("latin-1")
    lines_per_page = 4000
    text_pages = [
        text2[i : i + lines_per_page] for i in range(0, len(text2), lines_per_page)
    ]
    pdf.set_font("Times", size=14)
    for text_page in text_pages:
        pdf.add_page()
        pdf.multi_cell(200, 10, txt=text_page, align="L")
    t = time.localtime()
    curr_time = time.strftime("%H-%M-%S", t)
    adr = str(adr).replace(" ", "_")
    adr = str(adr).replace(".", "")
    name = f"certificate/cert_{adr}_{curr_time}.pdf"
    pdf.output(f"{name}", "F")
    return name
