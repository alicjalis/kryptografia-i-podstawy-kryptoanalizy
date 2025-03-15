import secrets

import numpy as np
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
import struct

# import secrets




AES_key = b'1234567890qwerty' # 16 bajtow - 128 bitow dla klucza
DES_key =b'12345678' # 8 bajtow, 56 bitow

matrix = np.zeros((64, 64))

def bytes_to_bin(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)


def generate_bit_flips(original_binary):
    binary_length = len(original_binary)
    flipped_messages = []

    for i in range(binary_length):
        flipped_bit = '0' if original_binary[i] == '1' else '1'  # Zamiana bitu
        new_binary = original_binary[:i] + flipped_bit + original_binary[i + 1:]  # Tworzenie nowego ciągu
        flipped_messages.append(new_binary)

    return flipped_messages

def encrypt_aes(input_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(input_text, 16))
    return bytes_to_bin(encrypted_message)

def encrypt_des(input_text, key):
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(input_text, 8))
    return bytes_to_bin(encrypted_message)

text = secrets.randbits(64)
input_text = text.to_bytes(8, byteorder="big")
text_binary = bytes_to_bin(input_text)


aes_output = encrypt_aes(input_text, AES_key)
des_output = encrypt_des(input_text, DES_key)

# Print the results
print("Random input as integer: ", text)
print("Random input in bits: ", text_binary)
print("Random input in bytes:", input_text)
print("AES encryption result:", aes_output)
print("DES encryption result:", des_output)