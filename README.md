✅ 1. Overview
  This solution:
  - Connects to an SFTP server using Paramiko.
  - Downloads files from a remote directory to a local directory.
  - Moves processed files to a backup directory on the SFTP server.
  - Uses encrypted password storage for security.

  Files:
  - encrypt_password.py → Generates encryption key and encrypts SFTP password.
  - sftp_config.json → Stores SFTP connection and path settings.
  - sftp_transfer.py → Main script for file transfer and backup.

---
✅ 2. Prerequisites
  - Python 3.8+
  - Install required packages:
      pip install paramiko cryptography
  - Ensure you have access to the SFTP server and correct credentials.

---
✅ 3. Configuration
  Step 3.1: Edit sftp_config.json
    Example:
      {
        "host": "10.1.10.80",
        "port": 222,
        "username": "username",
        "remotepath": "/source_path/New",
        "backuppath": "/source_path/Backup",
        "local_path": "X:/target_directory"
      }

---
✅ 4. Secure Password Setup
  Run encrypt_password.py:
    python encrypt_password.py
  What it does:
    - Generates sftp_key.key (encryption key).
    - Encrypts your password and saves it in sftp_password.enc.

**Important**: Replace "password" in encrypt_password.py with your actual SFTP password before running.

---
⚠️ Security Best Practice
  - After generating sftp_key.key and sftp_password.enc, delete or securely store encrypt_password.py.
  - Why?
      - The script contains hardcoded password logic, which is a security risk.
      - If someone reruns it, they could overwrite your encryption key or encrypted password.
  - Alternative: Remove the hardcoded password and keep the script only as a reusable utility, but restrict access.

---
✅ 5. Main Script Execution
  Run:
    python sftp_transfer.py
  What happens:
    - Loads config from sftp_config.json.
    - Decrypts password using sftp_key.key and sftp_password.enc.
    - Connects to SFTP server.
    - Checks if files in remote_path are stable (not recently modified).
    - Downloads stable files to local_path.
    - Moves processed files to backup_path.

---
✅ 6. Key Features
  - File Stability Check: Ensures files are older than 30 seconds before processing.
  - Backup Handling: Creates backup directory if missing.
  - Secure Authentication: Password never stored in plain text.

---
✅ 7. Best Practices
  - Store sftp_key.key and sftp_password.enc in a secure location.
  - Use environment variables for paths if possible.
  - Schedule the script using Task Scheduler (Windows) or cron (Linux).