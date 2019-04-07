from flask import Flask, render_template
from flask import request
from flask_socketio import SocketIO
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
app.config['FLASK_ENV'] = 'production'
app.config['FLASK_DEBUG'] = 1
socketio = SocketIO(app)

log_pos = 0


class LogChangeHandler(PatternMatchingEventHandler):

    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False,
                 case_sensitive=False):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_modified(self, event):
        global log_pos
        socketio.emit('my response', "logPos" + str(log_pos))
        with open(event.src_path) as f:
            f.seek(log_pos, 0)
            for i in f.readlines():
                socketio.emit('my response', i)
            log_pos = f.seek(0, 2)


@app.route('/')
def root():
    initial_log = []
    global log_pos
    with open("logs/testing.log") as f:
        for i in f.readlines():
            initial_log.append(i)
        log_pos = f.seek(0, 2)
    return render_template('static.html', initial_log=initial_log)


@app.route('/ping')
def handle_my_custom_event():
    print(request.args)
    socketio.emit('my response', "testing response")
    return ""


log_observer = Observer()
log_observer.schedule(
    LogChangeHandler(
        patterns=["*.log"],
        ignore_patterns=["*.swp"],
        ignore_directories=True,
        case_sensitive=True
    ),
    "logs",
    recursive=False
)
log_observer.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
    log_observer.stop()
    log_observer.join()
