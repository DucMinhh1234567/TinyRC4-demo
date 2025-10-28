"""
Flask Web Application for TinyRC4 Visualizer
"""

from flask import Flask, render_template, request, jsonify
from tinyrc4 import TinyRC4
import json

app = Flask(__name__)
rc4 = TinyRC4()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    """API endpoint for instant encryption."""
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '').strip()
        key = data.get('key', '').strip()
        
        if not plaintext or not key:
            return jsonify({
                'success': False,
                'error': 'Plaintext and key are required'
            })
        
        result = rc4.encrypt(plaintext, key)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """API endpoint for instant decryption."""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '').strip()
        key = data.get('key', '').strip()
        
        if not ciphertext or not key:
            return jsonify({
                'success': False,
                'error': 'Ciphertext and key are required'
            })
        
        result = rc4.decrypt(ciphertext, key)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/encrypt-steps', methods=['POST'])
def api_encrypt_steps():
    """API endpoint for step-by-step encryption."""
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '').strip()
        key = data.get('key', '').strip()
        
        if not plaintext or not key:
            return jsonify({
                'success': False,
                'error': 'Plaintext and key are required'
            })
        
        result = rc4.encrypt_with_steps(plaintext, key)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/decrypt-steps', methods=['POST'])
def api_decrypt_steps():
    """API endpoint for step-by-step decryption."""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '').strip()
        key = data.get('key', '').strip()
        
        if not ciphertext or not key:
            return jsonify({
                'success': False,
                'error': 'Ciphertext and key are required'
            })
        
        result = rc4.decrypt_with_steps(ciphertext, key)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


