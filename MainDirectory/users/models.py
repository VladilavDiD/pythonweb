# users/models.py
import hashlib, binascii, secrets

class User:
    def __init__(self, username, password=None, role="user"):
        self.username = username
        self.role = role
        self.password_hash = None
        if password:
            self.set_password(password)

    def set_password(self, password):
        salt = secrets.token_bytes(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
        self.password_hash = binascii.hexlify(salt + dk).decode()

    def check_password(self, password):
        raw = binascii.unhexlify(self.password_hash.encode())
        salt, stored = raw[:16], raw[16:]
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
        return secrets.compare_digest(dk, stored)
