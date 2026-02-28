import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


FOLDER_TO_TRACK = "C:\\Users\\hugol\\OneDrive\\Desktop\\TestDownloads"


FOLDER_MAPPING = {
    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".jpg": "Images",
    ".png": "Images",
    ".mp4": "Videos",
    ".zip": "Archives",
}

def move_file(file_path):
    
    if os.path.isdir(file_path): 
        return
    
    filename = os.path.basename(file_path)
    
    extension = os.path.splitext(filename)[1].lower()

    if extension in FOLDER_MAPPING:
        target_folder = os.path.join(FOLDER_TO_TRACK, FOLDER_MAPPING[extension])
        os.makedirs(target_folder, exist_ok=True)

        destination = os.path.join(target_folder, filename)
        if os.path.exists(destination):
            print(f"Skipping {filename}, already exists in destination.")
            return

        print(f"Moving {filename} to {FOLDER_MAPPING[extension]}/")
        shutil.move(file_path, destination)


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
       
        if not event.is_directory:
            time.sleep(1)
           
            move_file(event.src_path)

if __name__ == "__main__":
    print(f"Monitoring folder: {FOLDER_TO_TRACK}")
        
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_TRACK, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping script.")
    
   
    observer.join()