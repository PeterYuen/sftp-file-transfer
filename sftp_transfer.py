import paramiko
import os
import time
import json
from cryptography.fernet import Fernet

# Load configuration
with open("sftp_config.json", "r") as config_file:
    config = json.load(config_file)

host = config["host"]
port = config["port"]
username = config["username"]
remote_path = config["remote_path"]
backup_path = config["backup_path"]
local_path = config["local_path"]

# Load and decrypt password
with open("sftp_key.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

with open("sftp_password.enc", "rb") as enc_file:
    encrypted_password = enc_file.read()

password = fernet.decrypt(encrypted_password).decode()

# Timestamp-based file stability check
def is_file_stable(sftp, path, min_age_seconds=30):
    try:
        attrs = sftp.stat(path)
        modified_time = attrs.st_mtime
        current_time = time.time()
        age = current_time - modified_time
        print(f"File: {path}")
        print(f"  Last modified: {time.ctime(modified_time)}")
        print(f"  Current time:  {time.ctime(current_time)}")
        print(f"  Age: {age:.2f} seconds")
        return age > min_age_seconds
    except IOError as e:
        print(f"Error checking file timestamp: {e}")
        return False

# Connect and process files
transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

# Ensure backup directory exists
try:
    sftp.listdir(backup_path)
except IOError:
    print(f"Creating backup directory: {backup_path}")
    sftp.mkdir(backup_path)

# List and process files
files = sftp.listdir(remote_path)
for file in files:
    remote_file = f"{remote_path}/{file}"
    local_file = os.path.join(local_path, file)
    backup_file = f"{backup_path}/{file}"

    print(f"Checking if {file} is stable...")
    if is_file_stable(sftp, remote_file):
        print(f"Downloading {file}...")
        sftp.get(remote_file, local_file)

        print(f"Moving {file} to backup...")
        sftp.rename(remote_file, backup_file)
    else:
        print(f"Skipping {file}, it may still be in use.")

sftp.close()
transport.close()
print("Download and move complete.")