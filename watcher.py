import os
import time
import queue
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

event_queue = queue.Queue()


class MyEventHandler(FileSystemEventHandler):
    def _enqueue_event(self, event: FileSystemEvent, timestamp: str):
        if event.src_path == os.getcwd():
            return
        event_queue.put((event, timestamp))

    def on_any_event(self, event: FileSystemEvent):
        self._enqueue_event(event, str(datetime.now()))


def start_watcher(path="."):
    observer = Observer()
    observer.schedule(MyEventHandler(), path, recursive=True)
    observer.start()
    return observer


if __name__ == "__main__":
    observer = start_watcher(".")
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
