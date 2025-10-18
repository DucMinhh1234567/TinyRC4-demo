
"""
TinyRC4 CLI Tool
Standalone command-line interface for TinyRC4 encryption/decryption
"""

import sys
from tinyrc4 import TinyRC4

def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("           TinyRC4 Encryption/Decryption Tool")
    print("=" * 60)
    print("Supports characters A-H (3-bit encoding: A=000, B=001, ..., H=111)")
    print("Key format: comma-separated integers 0-7 (e.g., 2,1,3)")
    print("=" * 60)

def print_result(result, operation):
    """Print formatted result."""
    if result['success']:
        print(f"\n✓ {operation} successful!")
        print("-" * 40)
        
        if operation == "Encryption":
            print(f"Plaintext:  {result['plaintext']} ({result['plaintext_binary']})")
            print(f"Ciphertext: {result['ciphertext']} ({result['ciphertext_binary']})")
        else:  # Decryption
            print(f"Ciphertext: {result['ciphertext']} ({result['ciphertext_binary']})")
            print(f"Plaintext:  {result['plaintext']} ({result['plaintext_binary']})")
        
        print(f"Key:        {result['key']}")
        print("-" * 40)
    else:
        print(f"\n✗ {operation} failed!")
        print(f"Error: {result['error']}")

def get_user_input(prompt, validator=None):
    """Get user input with optional validation."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("Input cannot be empty. Please try again.")
                continue
            
            if validator:
                validator(value)
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)

def validate_text(text):
    """Validate text input (A-H characters only)."""
    text = text.upper()
    valid_chars = set('ABCDEFGH')
    invalid_chars = set(text) - valid_chars
    
    if invalid_chars:
        raise ValueError(f"Invalid characters: {', '.join(invalid_chars)}. Only A-H allowed.")
    
    return text

def validate_key(key_str):
    """Validate key input."""
    try:
        key_parts = [int(x.strip()) for x in key_str.split(',')]
        for k in key_parts:
            if not 0 <= k <= 7:
                raise ValueError(f"Key values must be 0-7, got {k}")
        if not 1 <= len(key_parts) <= 8:
            raise ValueError("Key must have 1-8 values")
        return key_str
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Key must contain only integers separated by commas")
        raise e

def main_menu():
    """Display main menu and handle user choice."""
    rc4 = TinyRC4()
    
    while True:
        print("\n" + "=" * 40)
        print("Main Menu:")
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Example (BAG with key 2,1,3)")
        print("4. Exit")
        print("=" * 40)
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            encrypt_text(rc4)
        elif choice == '2':
            decrypt_text(rc4)
        elif choice == '3':
            run_example(rc4)
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

def encrypt_text(rc4):
    """Handle text encryption."""
    print("\n--- Encryption ---")
    
    plaintext = get_user_input(
        "Enter plaintext (A-H characters only): ",
        validate_text
    )
    
    key = get_user_input(
        "Enter key (comma-separated 0-7 integers, e.g., 2,1,3): ",
        validate_key
    )
    
    result = rc4.encrypt(plaintext, key)
    print_result(result, "Encryption")

def decrypt_text(rc4):
    """Handle text decryption."""
    print("\n--- Decryption ---")
    
    ciphertext = get_user_input(
        "Enter ciphertext (A-H characters only): ",
        validate_text
    )
    
    key = get_user_input(
        "Enter key (comma-separated 0-7 integers, e.g., 2,1,3): ",
        validate_key
    )
    
    result = rc4.decrypt(ciphertext, key)
    print_result(result, "Decryption")

def run_example(rc4):
    """Run the lecture example."""
    print("\n--- Example from Lecture ---")
    print("Plaintext: BAG")
    print("Key: 2,1,3")
    print("Expected ciphertext: EBA")
    
    result = rc4.encrypt("BAG", "2,1,3")
    print_result(result, "Encryption")
    
    if result['success']:
        print("\nVerifying with decryption:")
        verify_result = rc4.decrypt(result['ciphertext'], "2,1,3")
        print_result(verify_result, "Decryption")

def main():
    """Main entry point."""
    try:
        print_banner()
        main_menu()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
