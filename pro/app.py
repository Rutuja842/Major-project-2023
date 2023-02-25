import os
import io
from flask import Flask, render_template, redirect, flash, request, send_from_directory, url_for, send_file, make_response
from werkzeug.utils import secure_filename
from utils import *
import re
from distutils.log import debug
from fileinput import filename
from PyPDF2 import PdfReader, PdfWriter
import docx2txt
import csv
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

email_regex = re.compile(r"[\w\.-]+@[\w\.-]+")
phone_num = re.compile(
    r'((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})|\d{5}-\d{6})')
url_https_regex = re.compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
url_regex = re.compile(r"\s*(www\.[^:\/\n]+\.\w+)\s*")
date_regex = re.compile(
    r"\d{2}[./-]\d{2}[./-]\d{4}|\d{4}[./-]\d{2}[./-]\d{2}|\d{1}[./-]\d{1}[./-]\d{4}|\d{4}[./-]\d{1}[./-]\d{1}|\d{2}[./-]\w+[./-]\d{4}|\w+[./-]\d{2}[./-]\d{4}|\d{4}[./-]\w+[./-]\d{2}")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['SECRET_KEY'] = 'my secret'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024


@app.route('/')
def main():
    return render_template("index.html")

#def export_to_csv(alldata, filename):
    alldata=[]
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        #print(type(result))
        if alldata:
            writer.writerow(alldata[0].keys())
            for row in alldata:
                writer.writerow(row.values())
            return file_path
        else:
            print("Result list is empty")
            return None
        

def process_image(path, filename):
    image = Image.open(path)
    text_to_display = pytesseract.image_to_string(image)
    return text_to_display


def process_docx(path, filename):
    text_to_display = docx2txt.process(path)
    print(text_to_display)
    return text_to_display


def process_txt(path, filename):
    txt_reader = open(path, 'rb')
    text_to_display = txt_reader.read()
    text_to_display = text_to_display.decode()
    return text_to_display


def process_pdf(path, filename):
    return extract_text(path, filename)


def extract_text(path, filename):
    pdf_reader = PdfReader(open(path, 'rb'))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page_num].extract_text()
        text_to_display = text
        return text_to_display


def processdata(choice, text_to_display):
    
    if choice == 'email':
        result = email_regex.findall(text_to_display)
        num_of_result = len(result)
    elif choice == 'phone':
        result = phone_num.findall(text_to_display)
        num_of_result = len(result)
    elif choice == 'url_https':
        result = url_https_regex.findall(text_to_display)
        num_of_result = len(result)
    elif choice == 'url':
        result = url_regex.findall(text_to_display)
        num_of_result = len(result)
    elif choice == 'date':
        result = date_regex.findall(text_to_display)
        num_of_result = len(result)
    elif choice == 'user_input':
        regex = request.form['regex']
        pattern = re.compile(regex)
        result = pattern.findall(text_to_display)
        num_of_result = len(result)
    return [result, num_of_result]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        choice = request.form['taskoption']

        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and file_valid(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if file.filename.endswith('.jpg'):
                content = process_image(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.jpeg'):
                content = process_image(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.gif'):
                content = process_image(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.png'):
                content = process_image(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.docx'):
                content = process_docx(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.txt'):
                content = process_txt(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.pdf'):
                content = process_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)


            alldata = processdata(choice,content)
            #csv_file = export_to_csv(alldata[0], filename='extracted_data.csv')
            #return send_file(csv_file, as_attachment=True, download_name='extracted_data.csv')
            return render_template('index.html', result=alldata[0],num_of_result = alldata[1])
          
        else:
            flash('Invalid file type')
            return redirect(request.url)




@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        choice = request.form['taskoption']
        if choice == 'email':
            rawtext = request.form['rawtext']
            results = email_regex.findall(rawtext)
            num_of_results = len(results)
        elif choice == 'phone':
            rawtext = request.form['rawtext']
            results = phone_num.findall(rawtext)
            num_of_results = len(results)
        elif choice == 'url_https':
            rawtext = request.form['rawtext']
            results = url_https_regex.findall(rawtext)
            num_of_results = len(results)
        elif choice == 'url':
            rawtext = request.form['rawtext']
            results = url_regex.findall(rawtext)
            num_of_results = len(results)
        elif choice == 'date':
            rawtext = request.form['rawtext']
            results = date_regex.findall(rawtext)
            num_of_results = len(results)



    return render_template("index.html", results=results,num_of_results = num_of_results)


if __name__ == '__main__':
    app.run(debug=True)
