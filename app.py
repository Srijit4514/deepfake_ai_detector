import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from transformers import pipeline
from PIL import Image
import librosa
import numpy as np

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Load models locally
print("Loading image detection model...")
try:
    image_classifier = pipeline("image-classification", model="dima806/ai_vs_real_image_detection")
    print("✓ Image model loaded successfully")
except Exception as e:
    print(f"✗ Error loading image model: {e}")
    image_classifier = None

print("Loading audio detection model...")
try:
    audio_classifier = pipeline("audio-classification", model="Gustking/wav2vec2-large-xlsr-deepfake-audio-classification")
    print("✓ Audio model loaded successfully")
except Exception as e:
    print(f"✗ Error loading audio model: {e}")
    audio_classifier = None


def allowed_file(filename, file_type):
    """Check if file extension is allowed."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if file_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'audio':
        return ext in ALLOWED_AUDIO_EXTENSIONS
    return False


def detect_image_deepfake(file_path):
    """Detect deepfake in image using local model."""
    if not image_classifier:
        return {'error': 'Image model not loaded'}
    
    try:
        # Load and process image
        image = Image.open(file_path).convert('RGB')
        
        # Run inference
        results = image_classifier(image)
        
        # Results is a list of dicts with 'label' and 'score'
        if results and len(results) > 0:
            # Find the prediction with highest score
            max_result = max(results, key=lambda x: x.get('score', 0))
            
            label = max_result.get('label', 'UNKNOWN')
            confidence = round(max_result.get('score', 0) * 100, 2)
            
            # If confidence is less than 70%, return REAL
            if confidence < 90:
                label = 'REAL'
            
            return {'label': label, 'confidence': confidence}
        
        return {'error': 'No predictions returned'}
    
    except Exception as e:
        return {'error': f'Error processing image: {str(e)}'}


def detect_audio_deepfake(file_path):
    """Detect deepfake in audio using local model."""
    if not audio_classifier:
        return {'error': 'Audio model not loaded'}
    
    try:
        # Load audio file
        audio_data, sr = librosa.load(file_path, sr=None)
        
        # Run inference
        results = audio_classifier(audio_data)
        
        # Results is a list of dicts with 'label' and 'score'
        if results and len(results) > 0:
            # Find the prediction with highest score
            max_result = max(results, key=lambda x: x.get('score', 0))
            
            label = max_result.get('label', 'UNKNOWN')
            confidence = round(max_result.get('score', 0) * 100, 2)
            
            # Treat low-confidence predictions as Fake
            if confidence < 80:
                label = 'Fake'
            return {'label': label, 'confidence': confidence}
        
        return {'error': 'No predictions returned'}
    
    except Exception as e:
        return {'error': f'Error processing audio: {str(e)}'}


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/detect/image', methods=['POST'])
def detect_image():
    """Endpoint for image deepfake detection."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename, 'image'):
            return jsonify({'success': False, 'error': 'Invalid file type. Use JPG or PNG.'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Detect deepfake using local model
            result = detect_image_deepfake(filepath)
            
            # Check for errors
            if 'error' in result:
                return jsonify({'success': False, 'error': result['error']}), 500
            
            return jsonify({
                'success': True,
                'label': result['label'],
                'confidence': result['confidence']
            }), 200
        
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/detect/audio', methods=['POST'])
def detect_audio():
    """Endpoint for audio deepfake detection."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename, 'audio'):
            return jsonify({'success': False, 'error': 'Invalid file type. Use WAV or MP3.'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Detect deepfake using local model
            result = detect_audio_deepfake(filepath)
            
            # Check for errors
            if 'error' in result:
                return jsonify({'success': False, 'error': result['error']}), 500
            
            return jsonify({
                'success': True,
                'label': result['label'],
                'confidence': result['confidence']
            }), 200
        
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
