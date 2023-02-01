import os
from flask import Flask, render_template, redirect, flash, request, send_from_directory,url_for
from werkzeug.utils import secure_filename
from utils import *
import re

email_regex = re.compile(r"[\w\.-]+@[\w\.-]+")
phone_num = re.compile(r'((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))')
url_https_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
url_regex = re.compile(r"\s*(www\.[^:\/\n]+\.\w+)\s*")
date_regex = re.compile(r"\d{2}[./-]\d{2}[./-]\d{4}|\d{4}[./-]\d{2}[./-]\d{2}|\d{1}[./-]\d{1}[./-]\d{4}|\d{4}[./-]\d{1}[./-]\d{1}|\d{2}[./-]\w+[./-]\d{4}|\w+[./-]\d{2}[./-]\d{4}|\d{4}[./-]\w+[./-]\d{2}")

app = Flask(__name__)
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER
app.config['SECRET_KEY'] = 'my secret'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024

#@app.route('/')
#def index():
	#return render_template("index.html")

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "GET":
    return render_template('index.html')
  
  if not 'file' in request.files:
    flash('No file part in request')
    return redirect(request.url)

  files = request.files.getlist('file')

  for file in files:
    if file.filename == '':
      flash('No file uploaded')
      return redirect(request.url)

    if file_valid(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
    else:
      flash('Invalid file type')
      return redirect(request.url) 
      
  return render_template("index.html")

@app.route('/uploads/<path:filename>')
def send_attachment(filename):
  return send_from_directory(app.config['UPLOADS_FOLDER'], 
    filename=filename, as_attachment=True)

@app.route('/process',methods=['POST'])
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
		
	
	return render_template("index.html",results=results,num_of_results = num_of_results)


if __name__ == '__main__':
	app.run(debug=True)