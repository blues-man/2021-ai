# If a file named wsgi.py is present in your repository, 
# it will be used as the entry point to your application. 
# This can be overridden with the environment variable APP_MODULE.
import json
from flask import Flask, jsonify, request
from prediction import predict, predict1, predict2, predict3
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

# v3
# The older model
# doesn't use ship_locations
# attacks center
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
    except Exception as e:
        print('ERROR!!!', e)
        return jsonify([])


# v4
# use ship_locations
# attacks center
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
        res = jsonify(predict2(data))
        return res
    except Exception as e:
        print('ERROR!!!', e)
        return jsonify([])


# v5
# use ship_locations
# attacks center+random
@application.route('/prediction3', methods=['POST'])
@timing
def object_detection3():
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    res = []
    try:
        print(data)
        # bState = data['board_state']
        res = jsonify(predict3(data))
        return res
    except Exception as e:
        print('ERROR!!!', e)
        return jsonify([])


# v6
# use ship_locations
# attacks based on previous probs then center
@application.route('/prediction', methods=['POST'])
def object_detection():
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    res = []
    try:
        print("model_v6")
        print(data)
        # bState = data['board_state']
        res = predict(data)
        res1 = jsonify(res)
        return res1
    except Exception as e:
        print('ERROR!!!', e)
        return jsonify([])
