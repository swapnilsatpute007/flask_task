from flask import Flask

UPLOAD_FOLDER = '/home/flask-task/upload_files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
