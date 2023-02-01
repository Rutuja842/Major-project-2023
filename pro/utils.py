ALLOWED_EXTENSIONS = ['pdf', 'docx']
UPLOADS_FOLDER = 'uploads/'
DOWNLOAD_FOLDER ='downloads/'

def file_valid(file):
  return '.' in file and \
    file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
