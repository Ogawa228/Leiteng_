import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_dir, file_name = os.path.split(file_path)
            file_name_without_ext, file_ext = os.path.splitext(file_name)
            current_date = time.strftime('%Y-%m-%d', time.localtime())
            new_file_name = f"{current_date}-{file_name}"
            new_file_path = os.path.join(file_dir, new_file_name)
            os.rename(file_path, new_file_path)


if __name__ == "__main__":
    path = r"C:\Users\Administrator\OneDrive\我的工作\雷腾律所mac"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  # 修改为recursive=True
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    