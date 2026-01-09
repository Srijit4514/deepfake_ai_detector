---
title: Deepfake Ai Detector
emoji: 📉
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: 6.2.0
app_file: app.py
pinned: false
license: mit
short_description: This is my first Space
---

# Deepfake Detector Website

A web-based application to detect AI-generated (fake) images and deepfake audio files using Hugging Face models.

## Features

- 🖼️ **Image Deepfake Detection** - Detect AI-generated images
- 🎵 **Audio Deepfake Detection** - Detect deepfake audio files
- 📊 **Confidence Scores** - Get detailed confidence percentages
- 🎨 **Clean UI** - Beautiful, responsive web interface
- ⚡ **Fast Processing** - Real-time analysis via Hugging Face API

## Models Used

- **Image Detection**: `dima806/ai_vs_real_image_detection`
- **Audio Detection**: `MelodyMachine/Deepfake-audio-detection-V2`

## Project Structure

```
deepfake-detector/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web UI
├── static/
│   └── script.js            # JavaScript logic
├── uploads/                 # Temporary file storage
└── README.md                # This file
```

## Installation & Setup

### 1. Get Hugging Face API Token

1. Go to https://huggingface.co and create an account
2. Navigate to Settings > Access Tokens
3. Create a new token with "Read" access
4. Copy your token

### 2. Set Environment Variable

**On Windows (PowerShell):**
```powershell
$env:HF_TOKEN = "your_hugging_face_token_here"
```

**On Windows (Command Prompt):**
```cmd
set HF_TOKEN=your_hugging_face_token_here
```

**On Mac/Linux:**
```bash
export HF_TOKEN="your_hugging_face_token_here"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Server

```bash
python app.py
```

You should see output like:
```
Running on http://127.0.0.1:5000
```

### 5. Open the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

## How to Use

### Image Detection
1. Click "Choose Image" or drag and drop a JPG/PNG file
2. Click "Analyze Image"
3. View the result with confidence percentage

### Audio Detection
1. Click "Choose Audio" or drag and drop a WAV/MP3 file
2. Click "Analyze Audio"
3. View the result with confidence percentage

## Supported File Types

- **Images**: JPG, PNG (max 10MB)
- **Audio**: WAV, MP3 (max 10MB)

## API Endpoints

### POST /detect/image
Analyzes an image for deepfakes.

**Request**: multipart/form-data with file
**Response**:
```json
{
  "success": true,
  "label": "FAKE",
  "confidence": 92.5
}
```

### POST /detect/audio
Analyzes audio for deepfakes.

**Request**: multipart/form-data with file
**Response**:
```json
{
  "success": true,
  "label": "REAL",
  "confidence": 87.3
}
```

## Troubleshooting

**"HF_TOKEN environment variable not set"**
- Make sure you've set the environment variable with your Hugging Face token

**"Model is loading. Please try again in a moment."**
- This happens on first use. Wait 30-60 seconds and try again

**Port 5000 already in use**
- Edit `app.py` and change `port=5000` to another port like `port=8000`

**Connection refused**
- Make sure Flask server is running: `python app.py`

## Requirements

- Python 3.8 or higher
- Hugging Face account (free)
- HF API token with Read access

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI Models**: Hugging Face Inference API
- **File Upload**: Werkzeug

## Notes

- Files are temporarily stored and automatically deleted after processing
- No data is permanently stored
- API token is kept secure in environment variable
- First API call may take 5-10 seconds (model warm-up)

## License

Models are used under their respective Hugging Face licenses.

---

**Built with Flask and Hugging Face 🚀**
