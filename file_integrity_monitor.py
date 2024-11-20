import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import smtplib
from email.mime.text import MIMEText


# def calculate_file_hash(filepath):
#     sha256_hash = hashlib.sha256()
#     with open(filepath, "rb") as f:
#         # Read and update hash in chunks to manage large files
#         for byte_block in iter(lambda: f.read(4096), b""):
#             sha256_hash.update(byte_block)
#     return sha256_hash.hexdigest()

def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except PermissionError:
        print(f"Permission denied for file: {filepath}. Retrying...")
        time.sleep(1)  # Wait for 1 second and retry
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()



class IntegrityMonitorHandler(FileSystemEventHandler):
    def __init__(self, monitored_files):
        super().__init__()
        self.monitored_files = monitored_files

    def on_modified(self, event):
        if event.is_directory:
            return None
        filepath = event.src_path
        new_hash = calculate_file_hash(filepath)
        
        if filepath in self.monitored_files:
            if self.monitored_files[filepath] != new_hash:
                print(f"File modified: {filepath}")
                self.monitored_files[filepath] = new_hash
                send_alert(filepath, "modified")
        else:
            self.monitored_files[filepath] = new_hash

    def on_deleted(self, event):
        if not event.is_directory:
            filepath = event.src_path
            if filepath in self.monitored_files:
                print(f"File deleted: {filepath}")
                send_alert(filepath, "deleted")
                del self.monitored_files[filepath]


    def on_created(self, event):
        if event.is_directory:
            return None
        filepath = event.src_path
        new_hash = calculate_file_hash(filepath)
        self.monitored_files[filepath] = new_hash
        print(f"File created: {filepath}")
        send_alert(filepath, "created")



import smtplib
from email.mime.text import MIMEText

def send_alert(filepath, action):
    sender_email = "sender@example.com"  # Enter your email
    sender_password = "your_app_specific_password"  # Use an app-specific password or an appropriate password
    receiver_email = "recipient@example.com"  # Enter receiver email
    
    # Construct the email content
    message = MIMEText(f"File {filepath} has been {action}.")
    message["Subject"] = f"File {filepath} {action}"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    try:
        # Connect to your local SMTP server running on port 1025
        with smtplib.SMTP("localhost", 1025) as server:
            # Login is not needed in your case since the local server doesn't require authentication
            # server.login(sender_email, sender_password)  # This line is not necessary
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")




def initialize_file_hashes(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hashes[filepath] = calculate_file_hash(filepath)
    return file_hashes

if __name__ == "__main__":
    directory_to_watch = r"C:\Users\vishakh\Desktop\seventh semester\cyber\t2"
    monitored_files = initialize_file_hashes(directory_to_watch)

    event_handler = IntegrityMonitorHandler(monitored_files)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
