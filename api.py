#!flask/bin/python
"""
scaffold for API endpoint. Browse to localhost:5000/api/test to view.
"""
from flask import Flask, jsonify
from flask import abort

app = Flask(__name__)

connections = [
    {
        'id': 1,
        'endpoint': u'2067e12fc5b99516e4971cfbdacfe75e',
    },
    {
        'id': 2,
        'endpoint': u'206dc79b92758760bd6df5c476796729',
    }
]


@app.route('/api/<path:uri>', methods=['GET'])
def get_task(uri):
    if len(uri) == 0:
        abort(404)
    return jsonify({'connections': connections})

if __name__ == '__main__':
    app.run(debug=True)
