import sys
import time
import pygame
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_callback):
        self.reload_callback = reload_callback

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"File changed: {event.src_path}")
            self.reload_callback()


def start_game():
    global main
    import main
    importlib.reload(main)
    main.run_game()


def watch_and_reload():
    event_handler = ReloadHandler(start_game)
    observer = Observer()
    observer.schedule(event_handler, path='./src', recursive=True)
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
