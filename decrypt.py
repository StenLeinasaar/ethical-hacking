import os
from cryptography.fernet import Fernet

# File paths
log_file = "keylog.txt"
key_file_path = "secret.key"

def load_key():
    if not os.path.exists(key_file_path):
        raise FileNotFoundError("Encryption key not found. Ensure 'secret.key' exists.")
    
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
    return key

def decrypt_log_file():
    key = load_key()
    cipher_suite = Fernet(key)
    
    if not os.path.exists(log_file):
        raise FileNotFoundError("Log file not found. Ensure 'keylog.txt' exists.")
    
    with open(log_file, "rb") as f:
        encrypted_data = f.read()
    
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
    except Exception as e:
        raise ValueError("Failed to decrypt the log file. Ensure the correct key is used.") from e

    decrypted_log_file = "decrypted_keylog.txt"
    with open(decrypted_log_file, "wb") as f:
        f.write(decrypted_data)
    
    print(f"Decrypted log file saved as '{decrypted_log_file}'")

if __name__ == "__main__":
    decrypt_log_file()
