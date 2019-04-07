import os
import time

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import request


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
app.config['FLASK_ENV'] = 'production'
app.config['FLASK_DEBUG'] = 1
socketio = SocketIO(app)


@app.route('/')
def root():
    initial_log = []
    with open("logs/testing.log") as f:
        for i in f.readlines():
            initial_log.append(i)
    return render_template('static.html', initial_log=initial_log)


@app.route('/ping')
def handle_my_custom_event():
    print(request.args)
    socketio.emit('my response', "testing response")
    return ""


if __name__ == '__main__':
    socketio.run(app, debug=True)
