from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def index():
    print(json.dumps(request.form))
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 3000, debug=True)