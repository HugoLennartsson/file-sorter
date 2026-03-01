import os
import shutil
import time
import json
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track, folder_mapping):
        self.folder_to_track = folder_to_track
        self.folder_mapping = folder_mapping

    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1) # Wait for download to finish
            self.move_file(event.src_path)

    def move_file(self, file_path):
        filename = os.path.basename(file_path)
        extension = os.path.splitext(filename)[1].lower()

        print(f"Detected new file: {filename} with extension: {extension}")

        if extension in self.folder_mapping:
            target_folder = os.path.join(self.folder_to_track, self.folder_mapping[extension])
            os.makedirs(target_folder, exist_ok=True)
            destination = os.path.join(target_folder, filename)
            
            if not os.path.exists(destination):
                shutil.move(file_path, destination)

class SorterInstance:
    def __init__(self):
        self.observer = None
        self.running = False

    def start(self):
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        event_handler = FileHandler(config["track_path"], config["mappings"])
        self.observer = Observer()
        self.observer.schedule(event_handler, config["track_path"], recursive=False)
        self.observer.start()
        self.running = True

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.running = False
    