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

    def sort_existing_files(self, folder_path, folder_mapping):
        """Sort all existing files in the given folder using the same rules as the live sorter."""
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}")
            return

        sorted_count = 0
        skipped_count = 0

        for item in os.listdir(folder_path):
            file_path = os.path.join(folder_path, item)

            # Skip directories
            if not os.path.isfile(file_path):
                continue

            extension = os.path.splitext(item)[1].lower()

            if extension in folder_mapping:
                target_folder = os.path.join(folder_path, folder_mapping[extension])
                os.makedirs(target_folder, exist_ok=True)
                destination = os.path.join(target_folder, item)

                if not os.path.exists(destination):
                    shutil.move(file_path, destination)
                    print(f"Sorted: {item} -> {folder_mapping[extension]}")
                    sorted_count += 1
                else:
                    print(f"Skipped (already exists): {item}")
                    skipped_count += 1
            else:
                print(f"No mapping for extension '{extension}', skipping: {item}")
                skipped_count += 1

        print(f"\nSorting complete: {sorted_count} files sorted, {skipped_count} files skipped")
        return sorted_count
    