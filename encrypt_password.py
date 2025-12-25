from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()
with open("sftp_key.key", "wb") as key_file:
    key_file.write(key)

# Encrypt password
fernet = Fernet(key)
password = "password"  # Replace with your actual password
encrypted = fernet.encrypt(password.encode())

with open("sftp_password.enc", "wb") as enc_file:
    enc_file.write(encrypted)

print("Password encrypted and saved.")