# cognitive_modules/stego_handler.py
from PIL import Image
import stepic
from cryptography.fernet import Fernet
import os

class StegoHandler:
    def __init__(self):
        # Manage encryption key
        self.key_file = "encryption.key"
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
        else:
            with open(self.key_file, "rb") as f:
                key = f.read()
        self.cipher = Fernet(key)

    def embed_message(self, img=None, save_path="outputs/hidden.png", message=""):
        # Encrypt the message
        encrypted_msg = self.cipher.encrypt(message.encode())

        # Create new image if none is provided
        if img is None:
            img = Image.new("RGB", (300, 300), color=(255, 255, 255))

        # Encode encrypted message in image
        encoded_img = stepic.encode(img, encrypted_msg)
        encoded_img.save(save_path, "PNG")
        return save_path

    def extract_message(self, img_path):
        img = Image.open(img_path)
        encrypted_msg = stepic.decode(img)
        try:
            decrypted_msg = self.cipher.decrypt(encrypted_msg).decode()
            return decrypted_msg
        except Exception:
            return "❌ Decryption failed or image corrupted"
