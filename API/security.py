from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b"1029479b78d145e1"  # 16 bytes key (hexadecimal)
key_qr = b'50645367566B5970'  # 16 bytes key (hexadecimal)

mode = AES.MODE_CBC

def encrypt(plaintext):
    cipher = AES.new(key, mode, key)
    padded_plaintext = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext.hex()

def decrypt(ciphertext):
    cipher = AES.new(key, mode, key)
    ciphertext_bytes = bytes.fromhex(ciphertext)
    padded_plaintext = cipher.decrypt(ciphertext_bytes)
    plaintext = unpad(padded_plaintext, AES.block_size).decode("utf-8")
    return plaintext

def encryptQR(plaintext):
    cipher = AES.new(key_qr, mode, key_qr)
    padded_plaintext = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext.hex()