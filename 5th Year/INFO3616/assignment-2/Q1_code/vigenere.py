LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def translate_message(key: str, message: str, mode: str) -> str:
    """
    `mode`: 'encrypt' or 'decrypt'
    """
    translated = []
    key_index = 0
    key_len = len(key)
    alpha_len = len(LETTERS)

    for ch in message:
        # Find position in alphabet
        idx = LETTERS.find(ch.upper())
        if idx == -1:
            # Not a letter: keep as-is, don't advance key
            translated.append(ch)
            continue

        shift = LETTERS.find(key[key_index])
        if mode == 'encrypt':
            idx = (idx + shift) % alpha_len
        elif mode == 'decrypt':
            idx = (idx - shift) % alpha_len
        else:
            raise ValueError("`mode` must be 'encrypt' or 'decrypt'.")

        # Preserve original case
        out = LETTERS[idx]
        translated.append(out if ch.isupper() else out.lower())

        # Advance key index only when a letter was processed
        key_index += 1
        if key_index == key_len:
            key_index = 0

    return ''.join(translated)

def encrypt_vigenere(plaintext: str, key: str) -> str:
    return translate_message(key, plaintext, 'encrypt')

def decrypt_vigenere(ciphertext: str, key: str) -> str:
    return translate_message(key, ciphertext, 'decrypt')

if __name__ == "__main__":
    KEY = "XVFERTQXSWIFMZQAB"
    with open("ciphertext.txt") as f:
        ciphertext = f.read()

    decrypted = decrypt_vigenere(ciphertext, KEY)
    print("Decrypted:")
    print(decrypted)