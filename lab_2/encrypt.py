def load_key_from_table(filename):
    key = {}
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) < 7:
            continue
        row = parts[0]
        letters = parts[1:7]
        for col, letter in enumerate(letters, start=1):
            if letter == 'пробел':
                letter = ' '
            if letter != '-':
                code = row + str(col)
                key[letter] = code
    return key


def encrypt_text(text, key):
    encrypted_parts = []
    for ch in text:
        if ch in key:
            encrypted_parts.append(key[ch])
        else:
            continue
    return ' '.join(encrypted_parts)


def decrypt_text(encrypted_text, key):
    reverse_key = {v: k for k, v in key.items()}
    decrypted_parts = []
    for code in encrypted_text.split():
        if code in reverse_key:
            decrypted_parts.append(reverse_key[code])
        else:
            continue
    return ''.join(decrypted_parts)


def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    key = load_key_from_table('key.txt')
    with open('input_text.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    encrypted = encrypt_text(text, key)
    save_to_file('encrypted.txt', encrypted)
    print("Зашифрованный текст сохранён в encrypted.txt")

    decrypted = decrypt_text(encrypted, key)
    save_to_file('decrypted_check.txt', decrypted)
    print("Расшифрованный текст сохранён в decrypted_check.txt")

    if decrypted == text:
        print("Расшифрованный текст совпадает с исходным.")
    else:
        print("Расшифрованный текст отличается от исходного!")


if __name__ == "__main__":
    main()