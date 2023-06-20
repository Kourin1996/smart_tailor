import os
import uuid
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from worker.main import start_project
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

app = Flask(__name__)
CORS(
    app
)

print('database for web server', os.path.abspath(os.path.join(os.getcwd(), "../database.json")))

@app.route('/')
def echo():
    id = str(uuid.uuid4())

    return jsonify({'message': 'hello', 'id': id})

@app.route('/debug', methods=['POST'])
def debug():
    id = str(uuid.uuid4())

    # content is dict
    content = request.json
    x = {'id': id}
    x.update(content)

    return jsonify(x)

@app.route('/projects', methods=['POST'])
def create_request():
    id = str(uuid.uuid4())

    record = {
        'id': id,
        'status': 'SETUP',
        'solidity_code': '',
        'react_code': '',
        'solidity_abi': '',
        'solidity_build_result': '',
        'react_build_result': ''
    }

    r.set(id, json.dumps(record))

    res = start_project.delay(
        id,
        request.json['query']
    )

    print('posted async job', res)

    return jsonify(record)

@app.route('/projects/<uuid>/status', methods=['GET'])
def get_record(uuid):
    raw_value = r.get(uuid)
    if raw_value is None:
        return jsonify(None)

    decoded = raw_value.decode()

    record = json.loads(decoded)

    return jsonify(record)


if __name__ == "__main__":
    app.run(port=8080, debug=True)