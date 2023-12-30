#!/usr/bin/env python3

from PIL import Image
from glob import glob
from fpdf import FPDF
from PyPDF2 import PdfMerger
import os

def delete_old_elements():
    if not any(os.listdir('./Output/')):
        print("[*] The /Output folder is already empty.")
        return

    for filename in os.listdir('./Output/'):
        file_path = os.path.join('./Output/', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def delete_reports():
    if not any(os.listdir('./Reports/')):
        print("[*] The /Reports folder is already empty.\n")
        return

    for filename in os.listdir('./Reports/'):
        file_path = os.path.join('./Reports/', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def png_to_pdf(domain):
    files = glob(os.path.join("./Output/", "*.png"))
    iml = []
    files = sorted(files, key=lambda x: os.stat(x).st_ctime, reverse=False)
    for img in files:
        imgs = Image.open(img)
        rgb_im = imgs.convert('RGB')  
        iml.append(rgb_im)

    pdf_path = os.path.join("./Reports/", f"report-images-{domain}.pdf")
    image = iml[0]
    iml.pop(0)
    image.save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=iml)

def txt_to_pdf(domain):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    files = glob(os.path.join("./Output/", "*.txt"))
    files = sorted(files, key=lambda x: os.stat(x).st_ctime, reverse=True)
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for x in f:
                pdf.cell(200, 4, txt=x, ln=1, align='L')
    pdf.output(f"./Reports/report-text-{domain}.pdf")

def merge(domain):
    pdfs = [f"./Reports/report-images-{domain}.pdf",f"./Reports/report-text-{domain}.pdf"]
    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write(f"./Reports/report-{domain}.pdf")
    os.remove(f"./Reports/report-text-{domain}.pdf")
    os.remove(f"./Reports/report-images-{domain}.pdf")
    print("[+] Full report generated in /Reports")
    merger.close()

def report(domain):
    saved_domain = domain
    has_png = any(".png" in filename for filename in os.listdir("./Output/"))
    has_txt = any(".txt" in filename for filename in os.listdir("./Output/"))

    if has_png and has_txt:
        print("Generating full report...")
        png_to_pdf(saved_domain)
        txt_to_pdf(saved_domain)
        merge(saved_domain)
    elif has_png:
        print("Generating image report...")
        png_to_pdf(saved_domain)
        print("[+] Image-only report generated in /Reports")
    elif has_txt:
        print("Generating text report...")
        txt_to_pdf(saved_domain)
        print("[+] Text-only report generated in /Reports")
