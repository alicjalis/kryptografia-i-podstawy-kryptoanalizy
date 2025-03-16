import secrets
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import struct

AES_key = b'1234567890qwerty'  # 16 bajtów (128 bitów)
matrix = np.zeros((64, 64))


def bytes_to_bin(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)

def bin_to_bytes(binary_data):
    return bytes(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))


def generate_bit_flips(original_binary):
    binary_length = len(original_binary)
    flipped_messages = []

    for i in range(binary_length):
        flipped_bit = '0' if original_binary[i] == '1' else '1'  # Zmiana bitu
        new_binary = original_binary[:i] + flipped_bit + original_binary[i + 1:]  # Nowy ciąg binarny
        flipped_messages.append(new_binary)

    return flipped_messages


def encrypt_aes(input_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(input_text, 16))
    return bytes_to_bin(encrypted_message)


def update_sac_matrix(original_binary, encrypted_messages, matrix):
    for i, encrypted_message in enumerate(encrypted_messages):
        # print("original_message: ", original_binary)
        # print("encrypted_message:", encrypted_message, "\n")

        # XOR między oryginalną zaszyfrowaną wiadomością a kolejnymi zaszyfrowanymi wiadomościami
        xor_result = int(original_binary, 2) ^ int(encrypted_message, 2)

        # Poprawa dzialania xor
        xor_result_binary = bin(xor_result)[2:].zfill(len(original_binary))  # Upewniamy się, że wynik jest 64-bitowy

        # Aktualizujemy macierz SAC: każdy kolejny wiersz macierzy to nowy xor
        for j in range(64):
            if xor_result_binary[j] == '1':
                matrix[i, j] += 1

for _ in range(2**20):
    # Generowanie losowego 64-bitowego tekstu
    text = secrets.randbits(64)
    input_text = text.to_bytes(8, byteorder="big")
    text_binary = bytes_to_bin(input_text)

    # Szyfrowanie oryginalnego tekstu AES
    aes_output = encrypt_aes(input_text, AES_key)

    # Generowanie wiadomości z pojedynczymi zmianami bitów
    flipped_messages = generate_bit_flips(text_binary)

    encrypted_messages = []
    for message in flipped_messages:
        message_bytes = bin_to_bytes(message)  # Konwersja binarnej wiadomości na bajty
        encrypted_message = encrypt_aes(message_bytes, AES_key)
        encrypted_messages.append(encrypted_message)

    update_sac_matrix(aes_output, encrypted_messages, matrix)


with open('matrix.txt', 'w') as f:
    for row in matrix:
        f.write(' '.join(map(str, row)) + '\n')


print("Random input as integer: ", text)
print("Random input in bits: ", text_binary)
print("Random input in bytes:", input_text)
print("AES encryption result (in bits):", aes_output)
print("SAC matrix after updates:\n", matrix)
