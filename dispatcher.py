import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class LogChangeHandler(PatternMatchingEventHandler):

    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False,
                 case_sensitive=False):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_modified(self, event):
        print(event.__dict__)

if __name__ == "__main__":
    log_observer = Observer()
    log_observer.schedule(
        LogChangeHandler(
            patterns="*.log",
            ignore_patterns="*.log.swp",
            ignore_directories=True,
            case_sensitive=True
        ),
        "logs",
        recursive=False
    )
    log_observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        log_observer.stop()
    log_observer.join()
