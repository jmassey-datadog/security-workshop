import logging

from datadog import initialize, statsd
from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

import utils

options = {
    'statsd_host':'datadog',
    'statsd_port':8125
}

logging.basicConfig(level=logging.INFO)

initialize(**options)


app = Flask(__name__)

# our setup has an upstream proxy. We use ProxyFix to set the request.remote_addr correctly
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    username = req_data.get('user')
    password = req_data.get('password')

    user = utils.check_login(username, password, request.remote_addr)

    if user:
        # add metric for failed login
        statsd.increment('login', tags=["outcome:success"])
        return jsonify({"outcome":"success"}), 200
    else:
        # add metric for successful login
        statsd.increment('login', tags=["outcome:failure"])
        return jsonify({"outcome":"failure"}), 401


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
