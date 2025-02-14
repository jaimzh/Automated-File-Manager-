import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

folder_path = r'C:\Users\Jaimz\Downloads\Automated Downloads'

downloaded_docs_folder = os.path.join(folder_path, "downloaded_docs")
downloaded_images_folder = os.path.join(folder_path, "downloaded_images")
downloaded_videos_folder = os.path.join(folder_path, "downloaded_videos")
downloaded_audio_folder = os.path.join(folder_path, "downloaded_audio")
downloaded_archives_folder = os.path.join(folder_path, "downloaded_archives")
downloaded_software_folder = os.path.join(folder_path, "downloaded_software")
downloaded_dumps = os.path.join(folder_path, "dumps")

class MyFileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"File or folder created: {event.src_path}")
        self.sort_file(event.src_path)

    def sort_file(self, file_path):
        if file_path.endswith((".txt", ".pdf", ".docx")):
            self.process_files(file_path, downloaded_docs_folder)
        elif file_path.endswith((".jpg", ".jpeg", ".png")):
            self.process_files(file_path, downloaded_images_folder)
        elif file_path.endswith((".mp4", ".mkv")):
            self.process_files(file_path, downloaded_videos_folder)
        elif file_path.endswith((".mp3", ".wav")):
            self.process_files(file_path, downloaded_audio_folder)
        elif file_path.endswith((".zip", ".rar")):
            self.process_files(file_path, downloaded_archives_folder)
        elif file_path.endswith((".exe")):
            self.process_files(file_path, downloaded_software_folder)
        else:
            self.process_files(file_path, downloaded_dumps)

    def process_files(self, file_path, organized_folder):
        if not os.path.exists(organized_folder):
            os.makedirs(organized_folder)

        file_name = os.path.basename(file_path)
        destination_filepath = os.path.join(organized_folder, file_name)

        # Handle duplicate files
        if os.path.exists(destination_filepath):
            base_name, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(destination_filepath):
                new_name = f"{base_name} ({counter}){ext}"
                destination_filepath = os.path.join(organized_folder, new_name)
                counter += 1

        # This handles the problem where the file is still downloading and still in use 
        while True:
            try:
                shutil.move(file_path, destination_filepath)
                break  # Exit the loop if the move is successful
            except PermissionError:
                print(f"File is in use, retrying: {file_path}")
                time.sleep(1)  # Wait for 1 second before retrying



def continuously_sort_files(): 
    while True:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if os.path.isfile(file_path):
                event_handler.sort_file(file_path)
        time.sleep(5)

# Main script
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    event_handler = MyFileEventHandler()

    # Start the watchdog observer
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()

    # Start the continuous sorting in parallel
    try:
        continuously_sort_files()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
