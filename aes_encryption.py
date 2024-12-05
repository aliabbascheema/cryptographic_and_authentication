from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

# Generate key and initialization vector
key = os.urandom(32)  # AES-256 key size
iv = os.urandom(16)   # Initialization vector for CBC mode

# Encrypt a message
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
padder = padding.PKCS7(128).padder()

message = b"This is a secret message!"
padded_message = padder.update(message) + padder.finalize()
ciphertext = encryptor.update(padded_message) + encryptor.finalize()

# Decrypt the message
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()
decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

# Unpad the decrypted message
unpadder = padding.PKCS7(128).unpadder()
unpadded_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

print(f"Original: {message}")
print(f"Encrypted: {ciphertext}")
print(f"Decrypted: {unpadded_message}")
