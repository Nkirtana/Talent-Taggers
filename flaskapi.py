from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

import os

# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
# https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api

app = Flask(__name__)
api = Api(app)

# file extensions API supports
ALLOWED_EXTENSIONS = {'.docx', '.pdf'}
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'static')

# Path where the files sent through api needs to be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# API class
class SkillExtract(Resource):

    @staticmethod
    def get():
        return {'message': 'API is up and running!'}

    @staticmethod
    def post():
        if request.method == 'POST':
            # print('POST request received')
            # print(request.files)
            if 'resume' not in request.files:
                return {'message': 'file in not present in request'}
            file = request.files['resume']
            if file.filename == '':
                return {'message': 'file in not selected'}
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.splitext(filepath)[-1].lower() in ALLOWED_EXTENSIONS:
                file.save(filepath)
            else:
                return {'message': f"File format {os.path.splitext(filepath)[-1]} not supported!"}

            return {'message': 'File loaded successfully!'}
            # os.remove(filepath)


# Routing for API
api.add_resource(SkillExtract, '/')

if __name__ == '__main__':
    app.run(debug=True)