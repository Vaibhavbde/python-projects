# ============================================================
# Level 3 - Task 2: Basic File Encryption / Decryption
# Codveda Python Development Internship
#
# Uses Fernet symmetric encryption (cryptography library).
# Fallback: pure-Python Caesar cipher (no dependencies).
#
# Install dependency for Fernet:
#   pip install cryptography
# ============================================================

import os
import sys

# ── Try to use Fernet; fall back to Caesar cipher ────────────
try:
    from cryptography.fernet import Fernet, InvalidToken
    USE_FERNET = True
except ImportError:
    USE_FERNET = False
    print("[Info] 'cryptography' package not found. Using Caesar cipher as fallback.")
    print("       To use Fernet, run: pip install cryptography\n")

KEY_FILE = "secret.key"

# ── Fernet helpers ────────────────────────────────────────────

def generate_key():
    """Generate and save a new Fernet key."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"🔑 New encryption key saved to '{KEY_FILE}'. Keep this safe!")
    return key

def load_key():
    """Load an existing Fernet key, or generate one if absent."""
    if not os.path.isfile(KEY_FILE):
        print(f"[Info] Key file '{KEY_FILE}' not found. Generating a new one …")
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def fernet_encrypt(input_path, output_path):
    key = load_key()
    f   = Fernet(key)
    with open(input_path, "rb") as fp:
        data = fp.read()
    encrypted = f.encrypt(data)
    with open(output_path, "wb") as fp:
        fp.write(encrypted)

def fernet_decrypt(input_path, output_path):
    key = load_key()
    f   = Fernet(key)
    with open(input_path, "rb") as fp:
        data = fp.read()
    try:
        decrypted = f.decrypt(data)
    except InvalidToken:
        raise ValueError(
            "Decryption failed. The file may be corrupted, "
            "or you are using the wrong key."
        )
    with open(output_path, "wb") as fp:
        fp.write(decrypted)

# ── Caesar cipher helpers (fallback) ─────────────────────────

SHIFT = 13   # ROT-13 — shift by any value you like

def caesar_char(char, shift):
    if char.isalpha():
        base  = ord("A") if char.isupper() else ord("a")
        return chr((ord(char) - base + shift) % 26 + base)
    return char

def caesar_encrypt_text(text, shift=SHIFT):
    return "".join(caesar_char(c, shift) for c in text)

def caesar_decrypt_text(text, shift=SHIFT):
    return caesar_encrypt_text(text, -shift)   # reverse shift

def caesar_encrypt(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as fp:
        text = fp.read()
    encrypted = caesar_encrypt_text(text)
    with open(output_path, "w", encoding="utf-8") as fp:
        fp.write(encrypted)

def caesar_decrypt(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as fp:
        text = fp.read()
    decrypted = caesar_decrypt_text(text)
    with open(output_path, "w", encoding="utf-8") as fp:
        fp.write(decrypted)

# ── Dispatcher ────────────────────────────────────────────────

def encrypt_file(input_path, output_path):
    if USE_FERNET:
        fernet_encrypt(input_path, output_path)
        print(f"🔒 Fernet-encrypted '{input_path}' → '{output_path}'")
    else:
        caesar_encrypt(input_path, output_path)
        print(f"🔒 Caesar-encrypted (shift={SHIFT}) '{input_path}' → '{output_path}'")

def decrypt_file(input_path, output_path):
    if USE_FERNET:
        fernet_decrypt(input_path, output_path)
        print(f"🔓 Fernet-decrypted '{input_path}' → '{output_path}'")
    else:
        caesar_decrypt(input_path, output_path)
        print(f"🔓 Caesar-decrypted (shift={SHIFT}) '{input_path}' → '{output_path}'")

# ── Input helpers ─────────────────────────────────────────────

def prompt_path(prompt, must_exist=True):
    while True:
        path = input(prompt).strip()
        if must_exist and not os.path.isfile(path):
            print(f"  [Error] File not found: '{path}'. Please try again.")
        else:
            return path

# ── Main ──────────────────────────────────────────────────────

def main():
    algo = "Fernet (symmetric)" if USE_FERNET else f"Caesar cipher (shift={SHIFT})"
    print("=" * 50)
    print("   File Encryption / Decryption Tool")
    print(f"   Algorithm: {algo}")
    print("=" * 50)
    print("\n  1. Encrypt a file")
    print("  2. Decrypt a file")
    print("  3. Exit")

    choice = input("\nYour choice (1-3): ").strip()

    if choice == "1":
        inp = prompt_path("Input file to encrypt: ", must_exist=True)
        out = input("Output (encrypted) file name: ").strip() or inp + ".enc"
        try:
            encrypt_file(inp, out)
        except Exception as e:
            print(f"[Error] {e}")

    elif choice == "2":
        inp = prompt_path("Input file to decrypt: ", must_exist=True)
        out = input("Output (decrypted) file name: ").strip() or inp + ".dec"
        try:
            decrypt_file(inp, out)
        except ValueError as e:
            print(f"[Error] {e}")
        except Exception as e:
            print(f"[Error] {e}")

    elif choice == "3":
        print("Goodbye!")

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
