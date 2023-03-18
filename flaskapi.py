from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

import os
from skillextractor import ExtractSkills
from filereader import ReadFiles
from onet.keyword_search import Onet

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

extract_skills_obj = ExtractSkills()

onet_obj = Onet()

# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
# https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
# https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/

app = Flask(__name__)
api = Api(app)

# file extensions API supports
ALLOWED_EXTENSIONS = {'.docx', '.pdf'}
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'static')

# Path where the files sent through api needs to be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"message": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# API class
class SkillExtractAPI(Resource):

    @staticmethod
    @jwt_required()
    def get():
        return {'message': 'API is up and running!'}

    @staticmethod
    @jwt_required()
    def post():
        if request.method == 'POST':
            # print('POST request received')
            # print(request.files)
            if 'resume' not in request.files:
                return {'message': 'file in not present in request'}
            file = request.files['resume']
            if file.filename == '':
                return {'message': 'file in not selected'}
            # To avoid malicious access to server directory
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.splitext(filepath)[-1].lower() in ALLOWED_EXTENSIONS:
                file.save(filepath)
            else:
                return {'message': f"File format {os.path.splitext(filepath)[-1]} not supported!"}

            file_reader_obj = ReadFiles(filepath)
            file_reader_obj.read_input()
            file_text = file_reader_obj.text_dict[filepath]

            os.remove(filepath)

            return extract_skills_obj.return_skills(file_text)


class OnetSkillsUpdationAPI(Resource):
    @staticmethod
    @jwt_required()
    def get():
        global extract_skills_obj
        message = onet_obj.update_skills_csv()
        extract_skills_obj = ExtractSkills()
        return message


# Routing for API
api.add_resource(SkillExtractAPI, '/')
api.add_resource(OnetSkillsUpdationAPI, '/updateskills')

if __name__ == '__main__':
    app.run(debug=True)
