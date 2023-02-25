ALLOWED_EXTENSIONS = ['pdf','txt', 'docx', 'png', 'jpg', 'jpeg', 'gif']
UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER ='downloads/'

def file_valid(file):
  return '.' in file and \
    file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


