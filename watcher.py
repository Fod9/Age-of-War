
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib

import main


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_callback):
        self.reload_callback = reload_callback

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.reload_callback()


def start_game():
    importlib.reload(main)
    main.main()


def watch_and_reload():
    event_handler = ReloadHandler(start_game)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_game()
    watch_and_reload()
