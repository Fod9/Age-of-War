import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import sys

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_event):
        self.reload_event = reload_event

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in: {event.src_path}")
            self.reload_event.set()

def start_watcher(reload_event):
    path = '.'
    event_handler = ReloadHandler(reload_event)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching for file changes in {os.path.abspath(path)}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
