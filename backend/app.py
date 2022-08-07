from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from FileProcessorSvc import FileProcessorSvc
from werkzeug.exceptions import BadRequestKeyError
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, 'files')

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

app = Flask(__name__)
CORS(app)


@app.route("/files", methods=['GET', 'POST'])  # POST = upload, GET = fetch all
def process_files():
    if request.method == 'POST':
        try:
            file = request.files['file']
        except KeyError:
            raise BadRequestKeyError
        path = os.path.join(FILES_DIR, file.filename)
        file.save(path)
        try:
            FileProcessorSvc.upload_file(file.filename, path)
        except Exception as e:
            print(e)
            if os.path.exists(path):
                os.remove(path)
            raise e
        resp = jsonify(success=True)
        resp.status_code = 201
        return resp

    return jsonify(files=FileProcessorSvc.get_all_file_names())


@app.route("/files/<file_name>", methods=['GET', 'DELETE'])  # GET = download one, DELETE = delete one
def process_file(file_name):
    if request.method == 'GET':
        file_url = FileProcessorSvc.get_download_url(file_name)
        return jsonify(url=file_url)
    elif request.method == 'DELETE':
        FileProcessorSvc.delete_file(file_name)
        return make_response(jsonify(success=True), 200)
    return make_response(jsonify(success=True), 404)

