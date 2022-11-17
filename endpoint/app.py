import os
from flask import Flask, flash, request, redirect, jsonify, url_for
from werkzeug.utils import secure_filename
from loader import Loader

UPLOAD_FOLDER = os.getcwd() + '/data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret_key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
   return ''

@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"response": "missing file key in request"})
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({"response": "missing file in request"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"response": "successfully saved the file"})
    else:
        return jsonify({"response": "file extension not allowed"})

@app.route('/upload_json', methods=['POST'])
def upload_json():
    input_data = request.get_json()

    entity = list(input_data.keys())[0]
    a = Loader(entity=entity, data=input_data[entity])

    return jsonify({"response": input_data})

if __name__== '__main__':
    app.run(debug=True)