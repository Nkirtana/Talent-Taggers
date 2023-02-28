from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class SkillExtract(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        if request.method == 'POST':
            print('POST request received')
            print(request.files)

api.add_resource(SkillExtract, '/')

if __name__ == '__main__':
    app.run(debug=True)