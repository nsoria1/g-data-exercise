import os
from flask import Flask, jsonify
from metrics import metric1, metric2

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route('/metric1', methods=['POST'])
def first_metric():
    result = metric1()
    if result is False:
        return jsonify({"response": "something failed while pulling the metric 1."})
    else:
        return jsonify(result)

@app.route('/metric2', methods=['POST'])
def second_metric():
    result = metric2()
    if result is False:
        return jsonify({"response": "something failed while pulling the metric 2."})
    else:
        return jsonify(result)

if __name__== '__main__':
    port = int(os.environ.get('PORT', 7000))
    app.run(debug=True, host='0.0.0.0', port=port)