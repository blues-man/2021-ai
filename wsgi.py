# If a file named wsgi.py is present in your repository, 
# it will be used as the entry point to your application. 
# This can be overridden with the environment variable APP_MODULE.
import json
from flask import Flask, jsonify, request
from prediction import predict, predict1
from functools import wraps
from time import time
application = Flask(__name__)

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %(f.__name__, args, kw, te-ts))
        return result
    return wrap


@application.route('/')
@application.route('/status')
@timing
def status():
    return jsonify({'status': 'ok'})

# The older model
# doesn't use ship_locations
@application.route('/prediction1', methods=['POST'])
@timing
def object_detection1():
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    res = []
    try:
        print(data)
        # bState = data['board_state']
        res = jsonify(predict1(data))
        return res
    except:
        print('ERROR!!!')
        return jsonify([])


# v5
# use ship_locations
#attacks center
@application.route('/prediction2', methods=['POST'])
@timing
def object_detection2():
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    res = []
    try:
        print(data)
        # bState = data['board_state']
        res = jsonify(predict1(data))
        return res
    except:
        print('ERROR!!!')
        return jsonify([])

# v5
# use ship_locations
#attacks random center or middle side rows
@application.route('/prediction', methods=['POST'])
@timing
def object_detection():
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    res = []
    try:
        print(data)
        # bState = data['board_state']
        res = jsonify(predict(data))
        return res
    except:
        print('ERROR!!!')
        return jsonify([])