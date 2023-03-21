import os
import io
from flask import Flask, render_template, redirect, flash, request, send_from_directory, url_for, send_file, make_response, session
from werkzeug.utils import secure_filename
from utils import *
import re
from distutils.log import debug
from fileinput import filename
from PyPDF2 import PdfReader, PdfWriter
import docx2txt
import pytesseract
from PIL import Image
import docx
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
app.config['SECRET_KEY'] = 'my secret'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024


@app.route('/')
def main():
    return render_template("index.html",result=[])


def process_image(path, filename):
    image = Image.open(path)
    text_to_display = pytesseract.image_to_string(image)
    return text_to_display


def process_docx(path, filename):
    text = docx2txt.process(path)
    
    doc = docx.Document(path)
    
    for para in doc.paragraphs:
        for run in para.runs:
            if run._element.tag.endswith('r'):
                for img in run._element.iter('pic:pic'):
                    img_data = img.find('pic:blipFill/a:blip/@r:embed', doc._part.rels).text
                    image_data = Image.open(io.BytesIO(doc.part.related_parts[img_data]._blob))
                    image_text = pytesseract.image_to_string(image_data)
                    text += "\n" + image_text
    
    text_to_display = text
    
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
        page = pdf_reader.pages[page_num]
        for image in page.images:
            img_data = image.data
            image_data = Image.open(io.BytesIO(img_data))
            image_text = pytesseract.image_to_string(image_data)
            text += image_text


        page_text = page.extract_text()
        if page_text:
            text += page_text

    text_to_display = text
    
    return text_to_display


def processdata(choice, text_to_display):
    result=[]
    num_of_result=0
    if choice == 'email':
        result += email_regex.findall(text_to_display)
        num_of_result += len(result)
    elif choice == 'phone':
        result += phone_num.findall(text_to_display)
        num_of_result += len(result)
    elif choice == 'url_https':
        result += url_https_regex.findall(text_to_display)
        num_of_result += len(result)
    elif choice == 'url':
        result += url_regex.findall(text_to_display)
        num_of_result += len(result)
    elif choice == 'date':
        result += date_regex.findall(text_to_display)
        num_of_result += len(result)
    elif choice == 'user_input':
        regex = request.form['regex']
        pattern = re.compile(regex)
        result += pattern.findall(text_to_display)
        num_of_result += len(result)
    result.insert(0, "No. of "+choice+" fetched "+str(num_of_result))
    return [result]



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

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
                content = process_image(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.jpeg'):
                content = process_image(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.gif'):
                content = process_image(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.png'):
                content = process_image(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.docx'):
                content = process_docx(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.txt'):
                content = process_txt(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), filename)

            if file.filename.endswith('.pdf'):
                content = process_pdf(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), filename)

            
            alldata=[]
            for key, val in request.form.items():
                if key.startswith("taskoption"):
                    print(key, val)
                    alldata += processdata(val,content)

            return render_template('index.html', result=alldata)
          
        else:
            flash('Invalid file type')
            return redirect(request.url)






if __name__ == '__main__':
    app.run(debug=True)
