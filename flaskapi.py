from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

import os


app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = {'docx', 'pdf'}
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'static')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class SkillExtract(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        if request.method == 'POST':
            print('POST request received')
            print(request.files)
            file = request.files['resume']
            print(file)
            filename = secure_filename(file.filename)
            print(filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

api.add_resource(SkillExtract, '/')

if __name__ == '__main__':
    app.run(debug=True)