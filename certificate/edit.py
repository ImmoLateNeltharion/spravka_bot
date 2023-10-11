import PyPDF2
import time

from fpdf import FPDF


def edit_cert(address):
    old_text = "______"
    pdf_file = PyPDF2.PdfReader(open("certificate/start.pdf", "rb"))
    page = pdf_file.pages[0]
    text = page.extract_text()
    str = f"{address}\nЗадолженность отсутствует."
    text = text.replace(old_text, str)
    return create_new_cert(text, address)


def create_new_cert(text, adr):
    pdf = FPDF()
    lines_per_page = 4000
    text_pages = [
        text[i : i + lines_per_page] for i in range(0, len(text), lines_per_page)
    ]
    pdf.add_font("TimesNew", "", "config/timesnewromanpsmt.ttf", uni=True)
    pdf.set_font("TimesNew", "", 14)
    for text_page in text_pages:
        pdf.add_page()
        pdf.multi_cell(200, 10, txt=text_page, align="C")
    t = time.localtime()
    curr_time = time.strftime("%H-%M-%S", t)
    adr = str(adr).replace(" ", "_")
    adr = str(adr).replace(".", "")
    name = f"certificate/cert_{adr}_{curr_time}.pdf"
    pdf.output(f"{name}", "F")
    return name
