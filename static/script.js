// IMAGE DETECTION
const imageInput = document.getElementById('imageInput');
const imageUploadArea = document.getElementById('imageUploadArea');
const imageFileName = document.getElementById('imageFileName');
const detectImageBtn = document.getElementById('detectImageBtn');
const imageLoading = document.getElementById('imageLoading');
const imageResult = document.getElementById('imageResult');
const imageError = document.getElementById('imageError');

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        imageFileName.textContent = `Selected: ${e.target.files[0].name}`;
    }
});

imageUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    imageUploadArea.style.background = '#f0f4ff';
});

imageUploadArea.addEventListener('dragleave', () => {
    imageUploadArea.style.background = 'white';
});

imageUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    imageUploadArea.style.background = 'white';
    imageInput.files = e.dataTransfer.files;
    if (imageInput.files.length > 0) {
        imageFileName.textContent = `Selected: ${imageInput.files[0].name}`;
    }
});

async function detectImage() {
    if (!imageInput.files.length) {
        imageError.textContent = 'Please select an image file';
        return;
    }

    const file = imageInput.files[0];
    
    // Validate file type
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
        imageError.textContent = 'Invalid file type. Please use JPG or PNG.';
        return;
    }

    // Validate file size
    if (file.size > 10 * 1024 * 1024) {
        imageError.textContent = 'File is too large. Maximum size is 10MB.';
        return;
    }

    clearImageResults();
    imageLoading.style.display = 'block';
    detectImageBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/detect/image', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayImageResult(data.label, data.confidence);
        } else {
            imageError.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        imageError.textContent = `Network error: ${error.message}`;
    } finally {
        imageLoading.style.display = 'none';
        detectImageBtn.disabled = false;
    }
}

function displayImageResult(label, confidence) {
    const resultClass = label.toUpperCase() === 'REAL' ? 'real' : 'fake';
    const resultText = label.toUpperCase() === 'REAL' 
        ? '✅ REAL - This image appears to be authentic' 
        : '⚠️ FAKE - This image appears to be AI-generated';

    imageResult.className = `result show ${resultClass}`;
    document.getElementById('imageLabel').textContent = resultText;
    document.getElementById('imageConfidenceText').textContent = `${confidence}%`;
    document.getElementById('imageConfidenceFill').style.width = `${confidence}%`;
    imageError.textContent = '';
}

function clearImageResults() {
    imageResult.classList.remove('show');
    imageError.textContent = '';
}

// AUDIO DETECTION
const audioInput = document.getElementById('audioInput');
const audioUploadArea = document.getElementById('audioUploadArea');
const audioFileName = document.getElementById('audioFileName');
const detectAudioBtn = document.getElementById('detectAudioBtn');
const audioLoading = document.getElementById('audioLoading');
const audioResult = document.getElementById('audioResult');
const audioError = document.getElementById('audioError');

audioInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        audioFileName.textContent = `Selected: ${e.target.files[0].name}`;
    }
});

audioUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    audioUploadArea.style.background = '#f0f4ff';
});

audioUploadArea.addEventListener('dragleave', () => {
    audioUploadArea.style.background = 'white';
});

audioUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    audioUploadArea.style.background = 'white';
    audioInput.files = e.dataTransfer.files;
    if (audioInput.files.length > 0) {
        audioFileName.textContent = `Selected: ${audioInput.files[0].name}`;
    }
});

async function detectAudio() {
    if (!audioInput.files.length) {
        audioError.textContent = 'Please select an audio file';
        return;
    }

    const file = audioInput.files[0];
    
    // Validate file type
    if (!['audio/wav', 'audio/mpeg'].includes(file.type)) {
        audioError.textContent = 'Invalid file type. Please use WAV or MP3.';
        return;
    }

    // Validate file size
    if (file.size > 10 * 1024 * 1024) {
        audioError.textContent = 'File is too large. Maximum size is 10MB.';
        return;
    }

    clearAudioResults();
    audioLoading.style.display = 'block';
    detectAudioBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/detect/audio', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayAudioResult(data.label, data.confidence);
        } else {
            audioError.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        audioError.textContent = `Network error: ${error.message}`;
    } finally {
        audioLoading.style.display = 'none';
        detectAudioBtn.disabled = false;
    }
}

function displayAudioResult(label, confidence) {
    const resultClass = label.toUpperCase() === 'REAL' ? 'real' : 'fake';
    const resultText = label.toUpperCase() === 'REAL' 
        ? '✅ REAL - This audio appears to be authentic' 
        : '⚠️ FAKE - This audio appears to be deepfake';

    audioResult.className = `result show ${resultClass}`;
    document.getElementById('audioLabel').textContent = resultText;
    document.getElementById('audioConfidenceText').textContent = `${confidence}%`;
    document.getElementById('audioConfidenceFill').style.width = `${confidence}%`;
    audioError.textContent = '';
}

function clearAudioResults() {
    audioResult.classList.remove('show');
    audioError.textContent = '';
}
