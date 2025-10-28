"""
TinyRC4 Algorithm Implementation
Based on the lecture material for educational visualization purposes.
"""

class TinyRC4:
    def __init__(self):
        # Character to 3-bit mapping (A=000, B=001, ..., H=111)
        self.char_to_bits = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 
            'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        self.bits_to_char = {v: k for k, v in self.char_to_bits.items()}
    
    def text_to_binary(self, text):
        """Convert text (A-H) to binary string representation."""
        binary_parts = []
        for char in text.upper():
            if char in self.char_to_bits:
                binary_parts.append(f"{self.char_to_bits[char]:03b}")
            else:
                raise ValueError(f"Invalid character '{char}'. Only A-H allowed.")
        return ''.join(binary_parts)
    
    def binary_to_text(self, binary_str):
        """Convert binary string to text (A-H)."""
        if len(binary_str) % 3 != 0:
            raise ValueError("Binary string length must be multiple of 3")
        
        text_parts = []
        for i in range(0, len(binary_str), 3):
            bit_group = binary_str[i:i+3]
            value = int(bit_group, 2)
            if value in self.bits_to_char:
                text_parts.append(self.bits_to_char[value])
            else:
                raise ValueError(f"Invalid binary value '{bit_group}'")
        return ''.join(text_parts)
    
    def parse_key(self, key_str):
        """Parse comma-separated key string to list of integers."""
        try:
            key_parts = [int(x.strip()) for x in key_str.split(',')]
            for k in key_parts:
                if not 0 <= k <= 7:
                    raise ValueError(f"Key values must be 0-7, got {k}")
            if not 1 <= len(key_parts) <= 8:
                raise ValueError("Key must have 1-8 values")
            return key_parts
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Key must contain only integers separated by commas")
            raise e
    
    def initialize_arrays(self, key):
        """Initialize S and T arrays according to TinyRC4 algorithm."""
        N = len(key)
        
        # Initialize S array with 0-7
        S = list(range(8))
        
        # Initialize T array with key repeated
        T = [key[i % N] for i in range(8)]
        
        return S, T
    
    def permute_s_array(self, S, T):
        """Permute S array based on T array."""
        j = 0
        for i in range(8):
            j = (j + S[i] + T[i]) % 8
            S[i], S[j] = S[j], S[i]  # Swap
        return S
    
    def generate_stream_with_steps(self, plaintext_binary, key):
        """Generate encryption stream with detailed step tracking."""
        steps = []
        
        # Convert plaintext to list of 3-bit integers
        plaintext_ints = []
        for i in range(0, len(plaintext_binary), 3):
            plaintext_ints.append(int(plaintext_binary[i:i+3], 2))
        
        # Initialize arrays
        S, T = self.initialize_arrays(key)
        
        # Add initialization step
        steps.append({
            'phase': 'init',
            'step_number': 0,
            'description': 'Initialize S and T arrays',
            'S': S.copy(),
            'T': T.copy(),
            'i': None,
            'j': None,
            'swap': None,
            't': None,
            'k': None,
            'k_binary': None
        })
        
        # Permute S array
        S = self.permute_s_array(S, T)
        
        # Add permutation step
        steps.append({
            'phase': 'init',
            'step_number': 1,
            'description': 'Permute S array based on T',
            'S': S.copy(),
            'T': T.copy(),
            'i': None,
            'j': None,
            'swap': None,
            't': None,
            'k': None,
            'k_binary': None
        })
        
        # Generate stream
        i, j = 0, 0
        stream = []
        
        for step_num, plaintext_int in enumerate(plaintext_ints):
            # Increment i
            i = (i + 1) % 8
            steps.append({
                'phase': 'generate',
                'step_number': step_num * 3 + 2,
                'description': f'Increment i: {i}',
                'S': S.copy(),
                'T': T.copy(),
                'i': i,
                'j': j,
                'swap': None,
                't': None,
                'k': None,
                'k_binary': None
            })
            
            # Update j
            j = (j + S[i]) % 8
            steps.append({
                'phase': 'generate',
                'step_number': step_num * 3 + 3,
                'description': f'Update j: j = (j + S[{i}]) mod 8 = ({j - S[i]} + {S[i]}) mod 8 = {j}',
                'S': S.copy(),
                'T': T.copy(),
                'i': i,
                'j': j,
                'swap': None,
                't': None,
                'k': None,
                'k_binary': None
            })
            
            # Swap S[i] and S[j]
            S[i], S[j] = S[j], S[i]
            steps.append({
                'phase': 'generate',
                'step_number': step_num * 3 + 4,
                'description': f'Swap S[{i}] and S[{j}]: {S[j]} ↔ {S[i]}',
                'S': S.copy(),
                'T': T.copy(),
                'i': i,
                'j': j,
                'swap': {'pos1': i, 'pos2': j},
                't': None,
                'k': None,
                'k_binary': None
            })
            
            # Calculate t and k
            t = (S[i] + S[j]) % 8
            k = S[t]
            k_binary = f"{k:03b}"
            
            steps.append({
                'phase': 'generate',
                'step_number': step_num * 3 + 5,
                'description': f'Calculate k: t = (S[{i}] + S[{j}]) mod 8 = ({S[i]} + {S[j]}) mod 8 = {t}, k = S[{t}] = {k} = {k_binary}',
                'S': S.copy(),
                'T': T.copy(),
                'i': i,
                'j': j,
                'swap': None,
                't': t,
                'k': k,
                'k_binary': k_binary
            })
            
            stream.append(k)
        
        return stream, steps
    
    def encrypt_with_steps(self, plaintext, key_str):
        """Encrypt plaintext with detailed step tracking."""
        try:
            key = self.parse_key(key_str)
            plaintext_binary = self.text_to_binary(plaintext)
            
            stream, steps = self.generate_stream_with_steps(plaintext_binary, key)
            
            # Convert plaintext binary to integers for XOR
            plaintext_ints = []
            for i in range(0, len(plaintext_binary), 3):
                plaintext_ints.append(int(plaintext_binary[i:i+3], 2))
            
            # Perform XOR
            ciphertext_ints = [p ^ s for p, s in zip(plaintext_ints, stream)]
            
            # Convert to binary string
            ciphertext_binary = ''.join(f"{c:03b}" for c in ciphertext_ints)
            ciphertext = self.binary_to_text(ciphertext_binary)
            
            return {
                'success': True,
                'plaintext': plaintext,
                'plaintext_binary': plaintext_binary,
                'ciphertext': ciphertext,
                'ciphertext_binary': ciphertext_binary,
                'key': key,
                'stream': stream,
                'steps': steps
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def decrypt_with_steps(self, ciphertext, key_str):
        """Decrypt ciphertext with detailed step tracking."""
        try:
            key = self.parse_key(key_str)
            ciphertext_binary = self.text_to_binary(ciphertext)
            
            stream, steps = self.generate_stream_with_steps(ciphertext_binary, key)
            
            # Convert ciphertext binary to integers for XOR
            ciphertext_ints = []
            for i in range(0, len(ciphertext_binary), 3):
                ciphertext_ints.append(int(ciphertext_binary[i:i+3], 2))
            
            # Perform XOR (same as encryption for stream ciphers)
            plaintext_ints = [c ^ s for c, s in zip(ciphertext_ints, stream)]
            
            # Convert to binary string
            plaintext_binary = ''.join(f"{p:03b}" for p in plaintext_ints)
            plaintext = self.binary_to_text(plaintext_binary)
            
            return {
                'success': True,
                'ciphertext': ciphertext,
                'ciphertext_binary': ciphertext_binary,
                'plaintext': plaintext,
                'plaintext_binary': plaintext_binary,
                'key': key,
                'stream': stream,
                'steps': steps
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def encrypt(self, plaintext, key_str):
        """Simple encryption without step tracking."""
        result = self.encrypt_with_steps(plaintext, key_str)
        if result['success']:
            return {
                'success': True,
                'plaintext': result['plaintext'],
                'plaintext_binary': result['plaintext_binary'],
                'ciphertext': result['ciphertext'],
                'ciphertext_binary': result['ciphertext_binary'],
                'key': result['key']
            }
        else:
            return result
    
    def decrypt(self, ciphertext, key_str):
        """Simple decryption without step tracking."""
        result = self.decrypt_with_steps(ciphertext, key_str)
        if result['success']:
            return {
                'success': True,
                'ciphertext': result['ciphertext'],
                'ciphertext_binary': result['ciphertext_binary'],
                'plaintext': result['plaintext'],
                'plaintext_binary': result['plaintext_binary'],
                'key': result['key']
            }
        else:
            return result


# Example usage and testing
if __name__ == "__main__":
    rc4 = TinyRC4()
    
    # Test with lecture example
    print("Testing TinyRC4 with lecture example:")
    print("Plaintext: BAG")
    print("Key: 2, 1, 3")
    
    result = rc4.encrypt_with_steps("BAG", "2, 1, 3")
    if result['success']:
        print(f"Plaintext: {result['plaintext']} ({result['plaintext_binary']})")
        print(f"Ciphertext: {result['ciphertext']} ({result['ciphertext_binary']})")
        print(f"Stream: {result['stream']}")
        print(f"Steps: {len(result['steps'])}")
    else:
        print(f"Error: {result['error']}")


