import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from loader import Loader

UPLOAD_FOLDER = os.getcwd() + '/data'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret_key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(req_file):
    if 'file' not in req_file:
        return jsonify({"response": "missing file key in request"})
    else:
        file = req_file['file']
        if file.filename == '':
            return jsonify({"response": "missing file in request"})
        else:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                try:
                    loader = Loader(path)
                except AssertionError:
                    return jsonify({"response": "filename was incorrect, please use correct filenames"})
                else:
                    loader.process_data()
                    status = loader.status
                    return jsonify({"response": f"successfully saved the file and processed it with status: {status}"})
            else:
                return jsonify({"response": "file extension not allowed"})

@app.route('/')
def index():
   return ''

@app.route('/upload', methods=['POST'])
def upload():
    return validate_file(request.files)

if __name__== '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)