// script.js
const dropbox = document.getElementById('dropbox');
const fileInput = document.getElementById('fileInput');
const resultContent = document.getElementById('resultContent');

// Drag and drop functionality
dropbox.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropbox.classList.add('dragover');
});

dropbox.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropbox.classList.remove('dragover');
});

dropbox.addEventListener('drop', (e) => {
    e.preventDefault();
    dropbox.classList.remove('dragover');
            
    const files = e.dataTransfer.files;
    if (files.length > 0) {
            handleFile(files[0]);
        }
});

// File input change
fileInput.addEventListener('change', (e) => {
if (e.target.files.length > 0) {
    handleFile(e.target.files[0]);
    }
});

// Click to upload
dropbox.addEventListener('click', () => {
    fileInput.click();
});

function handleFile(file) {
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload PNG, JPG, or JPEG images only.');
        return;
    }

    // Validate file size (optional - 5MB limit)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        showError('File too large. Please upload images smaller than 5MB.');
        return;
    }

    // Show loading state
    showLoading();
    dropbox.classList.add('uploading');

    // Convert to base64 and send to backend
    const reader = new FileReader();
    reader.onload = function(e) {
        const base64Data = e.target.result;
        classifyImage(base64Data);
        };

    reader.onerror = function() {
        showError('Error reading file. Please try again.');
        dropbox.classList.remove('uploading');
        };

    reader.readAsDataURL(file);
            }

async function classifyImage(base64Data) {
    try {
        // Send to Flask backend
        const response = await fetch('/classify_endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                },
            body: JSON.stringify({
                image: base64Data
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        displayResult(result);

    } catch (error) {
        console.error('Classification error:', error);
        showError(`Classification failed: ${error.message}`);
    } finally {
        dropbox.classList.remove('uploading');
    }
}

    function displayResult(result) {
        // Clear previous results
        resultContent.innerHTML = '';

        // Check for errors
        if (result.error) {
            showError(result.error);
                eturn;
        }

        // Check if we have the expected format
        if (!result.predicted_class || !result.confidence) {
            showError('Unexpected response format from server');
            return;
        }

        // Display celebrity name and confidence
        const celebrityDiv = document.createElement('div');
        celebrityDiv.className = 'result-celebrity';
        celebrityDiv.textContent = result.predicted_class;

        const probabilityDiv = document.createElement('div');
        probabilityDiv.className = 'result-probability';
        probabilityDiv.textContent = `Confidence: ${(result.confidence * 100).toFixed(1)}%`;

        resultContent.appendChild(celebrityDiv);
        resultContent.appendChild(probabilityDiv);

        // Display all class probabilities if available
        if (result.class_probabilities) {
            const detailsDiv = document.createElement('div');
            detailsDiv.className = 'result-details';

            Object.entries(result.class_probabilities).forEach(([name, prob]) => {
                const item = document.createElement('div');
                item.className = 'probability-item';
                    
                const nameSpan = document.createElement('div');
                nameSpan.className = 'probability-name';
                nameSpan.textContent = name;
                    
                const valueSpan = document.createElement('div');
                valueSpan.className = 'probability-value';
                valueSpan.textContent = `${(prob * 100).toFixed(1)}%`;
                    
                item.appendChild(nameSpan);
                item.appendChild(valueSpan);
                detailsDiv.appendChild(item);
            });

            resultContent.appendChild(detailsDiv);
        }

        // Add input type info if available
        if (result.input_type) {
            const infoDiv = document.createElement('div');
            infoDiv.style.marginTop = '15px';
            infoDiv.style.fontSize = '0.9rem';
            infoDiv.style.color = '#666';
            infoDiv.textContent = `Input type: ${result.input_type}`;
            resultContent.appendChild(infoDiv);
        }
    }

    function showError(message) {
        resultContent.innerHTML = `
            <div class="error-message">
                ❌ ${message}
            </div>
        `;
    }

    function showLoading() {
        resultContent.innerHTML = `
            <div class="loading">
                🔄 Classifying image...
            </div>
        `;
    }
