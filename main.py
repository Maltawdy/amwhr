from flask import Flask, request, abort
from functools import wraps
import os

app = Flask(__name__)

USERNAME = os.getenv("WEBHOOK_USER", "alertuser")
PASSWORD = os.getenv("WEBHOOK_PASS", "secretpass")

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            abort(401)
        return f(*args, **kwargs)
    return decorated

@app.route('/alert', methods=['POST'])
@require_auth
def alert():
    data = request.json
    print("Received alert:", data)
    return "Alert received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
