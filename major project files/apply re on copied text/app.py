from flask import Flask,render_template,url_for,request
import re

email_regex = re.compile(r"[\w\.-]+@[\w\.-]+")
phone_num = re.compile(r'((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))')
url_https_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
url_regex = re.compile(r"\s*(www\.[^:\/\n]+\.com)\s*")
date_regex = re.compile(r"\d{2}[./-]\d{2}[./-]\d{4}|\d{4}[./-]\d{2}[./-]\d{2}|\d{1}[./-]\d{1}[./-]\d{4}|\d{4}[./-]\d{1}[./-]\d{1}|\d{2}[./-]\w+[./-]\d{4}|\w+[./-]\d{2}[./-]\d{4}|\d{4}[./-]\w+[./-]\d{2}")

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

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