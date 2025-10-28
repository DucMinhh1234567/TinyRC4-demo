# TinyRC4 Visualizer System

An educational web application and command-line tool for visualizing the TinyRC4 stream cipher algorithm with step-by-step animation.

## Features

### Web Application
- **Instant Mode**: Quick encryption/decryption with immediate results
- **Step-by-Step Visualizer**: Animated visualization with:
  - Play/pause controls with adjustable speed (0.5x, 1x, 2x, 4x)
  - Step-by-step navigation (previous/next)
  - Multiple detail levels (phases only, per step, all substeps, full detail)
  - Real-time array visualization with highlighting
  - Interactive S and T array displays
  - Variable tracking (i, j, t, k values)

### Command-Line Tool
- Interactive menu-driven interface
- Input validation for text (A-H characters) and keys (0-7 integers)
- Both text and binary representation display
- Built-in example demonstration

## Algorithm Details

TinyRC4 is a simplified version of the RC4 stream cipher designed for educational purposes:

- **Character Set**: 8 characters (A-H) encoded as 3-bit values (000-111)
- **Key Format**: 1-8 integers, each ranging from 0-7
- **Arrays**: S and T arrays of size 8
- **Process**: Initialization phase followed by stream generation

### Example
- Plaintext: "BAG" (001 000 110)
- Key: 2, 1, 3
- Ciphertext: "EBA" (100 001 000)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project files**
   ```bash
   # Ensure you have all the following files:
   # - app.py
   # - tinyrc4.py
   # - cli.py
   # - requirements.txt
   # - templates/index.html
   # - static/css/style.css
   # - static/js/visualizer.js
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web application**
   ```bash
   python app.py
   ```
   The web interface will be available at `http://localhost:5000`

4. **Run the command-line tool**
   ```bash
   python cli.py
   ```

## Usage

### Web Application

1. **Instant Mode**:
   - Select Encrypt or Decrypt
   - Enter text (A-H characters only)
   - Enter key (comma-separated 0-7 integers, e.g., "2,1,3")
   - Click "Process" to see immediate results

2. **Step-by-Step Visualizer**:
   - Select Encrypt or Decrypt
   - Enter text and key
   - Click "Start Visualization"
   - Use controls to navigate through steps:
     - **Play/Pause**: Auto-play through steps
     - **Previous/Next**: Manual step navigation
     - **Speed**: Adjust playback speed
     - **Detail Level**: Choose visualization detail
     - **Reset**: Return to first step

### Command-Line Tool

Run `python cli.py` and follow the interactive menu:

1. **Encrypt text**: Enter plaintext and key
2. **Decrypt text**: Enter ciphertext and key
3. **Example**: Run the built-in "BAG" example
4. **Exit**: Quit the application

## File Structure

```
/
├── app.py                 # Flask web server
├── tinyrc4.py            # Core TinyRC4 algorithm implementation
├── cli.py                # Command-line interface
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface template
└── static/
    ├── css/
    │   └── style.css     # Styling and animations
    └── js/
        └── visualizer.js # Visualization logic
```

## API Endpoints

The Flask application provides the following REST API endpoints:

- `POST /api/encrypt` - Instant encryption
- `POST /api/decrypt` - Instant decryption
- `POST /api/encrypt-steps` - Step-by-step encryption data
- `POST /api/decrypt-steps` - Step-by-step decryption data

### API Request Format
```json
{
  "plaintext": "BAG",  // or "ciphertext" for decryption
  "key": "2,1,3"
}
```

### API Response Format
```json
{
  "success": true,
  "plaintext": "BAG",
  "plaintext_binary": "001000110",
  "ciphertext": "EBA",
  "ciphertext_binary": "100001000",
  "key": [2, 1, 3],
  "stream": [5, 1, 6],
  "steps": [...]  // Only for step endpoints
}
```

## Educational Value

This tool is designed to help students understand:

1. **Stream Cipher Concepts**: How stream ciphers generate pseudo-random sequences
2. **Array Operations**: S and T array initialization and permutation
3. **XOR Operations**: How plaintext is combined with the stream
4. **Algorithm Steps**: Detailed breakdown of each operation
5. **Visual Learning**: Interactive visualization of abstract concepts

## Technical Details

### TinyRC4 Algorithm Steps

1. **Initialization**:
   - Initialize S array with values 0-7
   - Initialize T array by repeating the key
   - Permute S array based on T array

2. **Stream Generation** (for each plaintext unit):
   - Increment i: `i = (i + 1) mod 8`
   - Update j: `j = (j + S[i]) mod 8`
   - Swap S[i] and S[j]
   - Calculate t: `t = (S[i] + S[j]) mod 8`
   - Generate k: `k = S[t]`

3. **Encryption/Decryption**:
   - XOR each plaintext unit with corresponding k value

## Troubleshooting

### Common Issues

1. **Invalid characters**: Only A-H characters are supported
2. **Invalid key format**: Use comma-separated integers 0-7
3. **Port already in use**: Change the port in `app.py` if 5000 is occupied
4. **Module not found**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Browser Compatibility

The web application works best with modern browsers that support:
- ES6 JavaScript features
- CSS Grid and Flexbox
- CSS Animations

## Contributing

This is an educational project. Feel free to:
- Report bugs or issues
- Suggest improvements to the visualization
- Add new educational features
- Improve the documentation

## License

This project is created for educational purposes. Feel free to use and modify for learning and teaching.

## References

Based on the lecture material "AN TOÀN VÀ BẢO MẬT THÔNG TIN - Chương 2: MÃ HOÁ KHOÁ ĐỐI XỨNG" covering TinyRC4 algorithm implementation.


