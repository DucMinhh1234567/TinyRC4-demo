/**
 * TinyRC4 Visualizer JavaScript
 * Handles the interactive visualization of TinyRC4 encryption/decryption
 */

class TinyRC4Visualizer {
    constructor() {
        this.currentSteps = [];
        this.currentStepIndex = 0;
        this.isPlaying = false;
        this.playInterval = null;
        this.currentSpeed = 1;
        this.currentDetailLevel = 'steps';
        
        this.initializeEventListeners();
        this.initializeTabs();
    }

    initializeEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Instant mode
        document.getElementById('instant-submit').addEventListener('click', () => {
            this.handleInstantMode();
        });

        // Visualizer mode
        document.getElementById('viz-submit').addEventListener('click', () => {
            this.handleVisualizerMode();
        });

        // Binary display updates
        document.getElementById('instant-text').addEventListener('input', (e) => {
            this.updateBinaryDisplay(e.target.value, 'instant-binary-display');
        });

        document.getElementById('viz-text').addEventListener('input', (e) => {
            this.updateBinaryDisplay(e.target.value, 'viz-binary-display');
        });

        // Visualizer controls
        document.getElementById('play-pause').addEventListener('click', () => {
            this.togglePlayPause();
        });

        document.getElementById('prev-step').addEventListener('click', () => {
            this.previousStep();
        });

        document.getElementById('next-step').addEventListener('click', () => {
            this.nextStep();
        });

        document.getElementById('reset').addEventListener('click', () => {
            this.resetVisualizer();
        });

        document.getElementById('speed').addEventListener('change', (e) => {
            this.currentSpeed = parseFloat(e.target.value);
            if (this.isPlaying) {
                this.startAutoPlay();
            }
        });

        document.getElementById('detail-level').addEventListener('change', (e) => {
            this.currentDetailLevel = e.target.value;
            this.filterSteps();
        });
    }

    initializeTabs() {
        // Set initial tab
        this.switchTab('instant');
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');
    }

    updateBinaryDisplay(text, displayId) {
        const display = document.getElementById(displayId);
        if (!text) {
            display.textContent = '';
            return;
        }

        try {
            const binary = this.textToBinary(text);
            display.textContent = `Binary: ${binary}`;
        } catch (error) {
            display.textContent = `Error: ${error.message}`;
        }
    }

    textToBinary(text) {
        const charToBits = {
            'A': '000', 'B': '001', 'C': '010', 'D': '011',
            'E': '100', 'F': '101', 'G': '110', 'H': '111'
        };
        
        const upperText = text.toUpperCase();
        const binaryParts = [];
        
        for (let char of upperText) {
            if (charToBits[char]) {
                binaryParts.push(charToBits[char]);
            } else {
                throw new Error(`Invalid character '${char}'. Only A-H allowed.`);
            }
        }
        
        return binaryParts.join('');
    }

    async handleInstantMode() {
        const operation = document.querySelector('input[name="operation"]:checked').value;
        const text = document.getElementById('instant-text').value.trim();
        const key = document.getElementById('instant-key').value.trim();

        if (!text || !key) {
            this.showError('instant-result', 'Please enter both text and key.');
            return;
        }

        try {
            const endpoint = operation === 'encrypt' ? '/api/encrypt' : '/api/decrypt';
            const dataKey = operation === 'encrypt' ? 'plaintext' : 'ciphertext';
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    [dataKey]: text,
                    key: key
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.showInstantResult(result, operation);
            } else {
                this.showError('instant-result', result.error);
            }
        } catch (error) {
            this.showError('instant-result', `Network error: ${error.message}`);
        }
    }

    showInstantResult(result, operation) {
        const resultDiv = document.getElementById('instant-result');
        const contentDiv = document.getElementById('instant-result-content');
        
        let html = '';
        if (operation === 'encrypt') {
            html = `
                <div class="success">
                    <strong>Encryption successful!</strong><br>
                    Plaintext: ${result.plaintext} (${result.plaintext_binary})<br>
                    Ciphertext: ${result.ciphertext} (${result.ciphertext_binary})<br>
                    Key: [${result.key.join(', ')}]
                </div>
            `;
        } else {
            html = `
                <div class="success">
                    <strong>Decryption successful!</strong><br>
                    Ciphertext: ${result.ciphertext} (${result.ciphertext_binary})<br>
                    Plaintext: ${result.plaintext} (${result.plaintext_binary})<br>
                    Key: [${result.key.join(', ')}]
                </div>
            `;
        }
        
        contentDiv.innerHTML = html;
        resultDiv.style.display = 'block';
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        const contentDiv = container.querySelector('.result-content') || container;
        
        contentDiv.innerHTML = `<div class="error">${message}</div>`;
        container.style.display = 'block';
    }

    async handleVisualizerMode() {
        const operation = document.querySelector('input[name="viz-operation"]:checked').value;
        const text = document.getElementById('viz-text').value.trim();
        const key = document.getElementById('viz-key').value.trim();

        if (!text || !key) {
            this.showError('visualizer-content', 'Please enter both text and key.');
            return;
        }

        try {
            const endpoint = operation === 'encrypt' ? '/api/encrypt-steps' : '/api/decrypt-steps';
            const dataKey = operation === 'encrypt' ? 'plaintext' : 'ciphertext';
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    [dataKey]: text,
                    key: key
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.initializeVisualizer(result, operation);
            } else {
                this.showError('visualizer-content', result.error);
            }
        } catch (error) {
            this.showError('visualizer-content', `Network error: ${error.message}`);
        }
    }

    initializeVisualizer(result, operation) {
        this.currentSteps = result.steps;
        this.currentStepIndex = 0;
        this.isPlaying = false;
        
        // Show visualizer section
        document.getElementById('visualizer-content').style.display = 'block';
        
        // Update step counter
        this.updateStepCounter();
        
        // Filter steps based on detail level
        this.filterSteps();
        
        // Show final result
        this.showVisualizerResult(result, operation);
        
        // Display first step
        this.displayCurrentStep();
    }

    filterSteps() {
        // This would filter steps based on detail level
        // For now, we'll show all steps
        this.filteredSteps = this.currentSteps;
        this.updateStepCounter();
    }

    updateStepCounter() {
        document.getElementById('current-step').textContent = this.currentStepIndex + 1;
        document.getElementById('total-steps').textContent = this.filteredSteps.length;
    }

    displayCurrentStep() {
        if (this.currentStepIndex >= this.filteredSteps.length) return;
        
        const step = this.filteredSteps[this.currentStepIndex];
        
        // Update description
        document.getElementById('step-description').textContent = step.description;
        
        // Update arrays
        this.updateArrayDisplay('s-array', step.S, step);
        this.updateArrayDisplay('t-array', step.T, step);
        
        // Update variables
        document.getElementById('var-i').textContent = step.i !== null ? step.i : '-';
        document.getElementById('var-j').textContent = step.j !== null ? step.j : '-';
        document.getElementById('var-t').textContent = step.t !== null ? step.t : '-';
        document.getElementById('var-k').textContent = step.k !== null ? step.k : '-';
        
        // Update step counter
        this.updateStepCounter();
    }

    updateArrayDisplay(arrayId, array, step) {
        const container = document.getElementById(arrayId);
        container.innerHTML = '';
        
        array.forEach((value, index) => {
            const cell = document.createElement('div');
            cell.className = 'array-cell';
            cell.textContent = value;
            
            // Add index label
            const indexLabel = document.createElement('div');
            indexLabel.className = 'array-index';
            indexLabel.textContent = index;
            cell.appendChild(indexLabel);
            
            // Add highlighting based on step
            if (step.i === index) {
                cell.classList.add('index-highlight');
            }
            if (step.j === index) {
                cell.classList.add('index-highlight');
            }
            if (step.swap && (step.swap.pos1 === index || step.swap.pos2 === index)) {
                cell.classList.add('swapped');
            }
            
            container.appendChild(cell);
        });
    }

    showVisualizerResult(result, operation) {
        const contentDiv = document.getElementById('viz-result-content');
        
        let html = '';
        if (operation === 'encrypt') {
            html = `
                <div class="success">
                    <strong>Encryption completed!</strong><br>
                    Plaintext: ${result.plaintext} (${result.plaintext_binary})<br>
                    Ciphertext: ${result.ciphertext} (${result.ciphertext_binary})<br>
                    Key: [${result.key.join(', ')}]<br>
                    Stream: [${result.stream.join(', ')}]
                </div>
            `;
        } else {
            html = `
                <div class="success">
                    <strong>Decryption completed!</strong><br>
                    Ciphertext: ${result.ciphertext} (${result.ciphertext_binary})<br>
                    Plaintext: ${result.plaintext} (${result.plaintext_binary})<br>
                    Key: [${result.key.join(', ')}]<br>
                    Stream: [${result.stream.join(', ')}]
                </div>
            `;
        }
        
        contentDiv.innerHTML = html;
    }

    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        this.isPlaying = true;
        document.getElementById('play-pause').textContent = '⏸️ Pause';
        this.startAutoPlay();
    }

    pause() {
        this.isPlaying = false;
        document.getElementById('play-pause').textContent = '▶️ Play';
        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }
    }

    startAutoPlay() {
        if (this.playInterval) {
            clearInterval(this.playInterval);
        }
        
        const interval = 1000 / this.currentSpeed; // Base interval is 1 second
        this.playInterval = setInterval(() => {
            if (this.currentStepIndex < this.filteredSteps.length - 1) {
                this.nextStep();
            } else {
                this.pause();
            }
        }, interval);
    }

    nextStep() {
        if (this.currentStepIndex < this.filteredSteps.length - 1) {
            this.currentStepIndex++;
            this.displayCurrentStep();
        }
    }

    previousStep() {
        if (this.currentStepIndex > 0) {
            this.currentStepIndex--;
            this.displayCurrentStep();
        }
    }

    resetVisualizer() {
        this.pause();
        this.currentStepIndex = 0;
        this.displayCurrentStep();
    }
}

// Initialize the visualizer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TinyRC4Visualizer();
});
