import os
from flask import Flask, jsonify
from backup import backup
from restore import restore

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route('/backup', methods=['POST'])
def backups():
    if backup():
        return jsonify({"response": "backups were taken sucessfully"})
    else:
        return jsonify({"response": "backups were not taken correctly"})

@app.route('/restore', methods=['POST'])
def restore_db():
    if restore():
        return jsonify({"response": "restore were sucessfully done"})
    else:
        return jsonify({"response": "restore was not applied correctly"})

if __name__== '__main__':
    port = int(os.environ.get('PORT', 6000))
    app.run(debug=True, host='0.0.0.0', port=port)