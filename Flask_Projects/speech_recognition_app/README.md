# Flask Speech Recognition App

A Flask-based web application for speech recognition, powered by Python's SpeechRecognition library. The app allows users to upload audio files, and it converts speech in the audio to text. The application has been containerized using Docker for easy deployment.

## Features
- Upload audio files (WAV, MP3, etc.) for speech-to-text conversion.
- Speech recognition powered by the `SpeechRecognition` library.
- Dockerized for easy deployment and scaling.

## Requirements
- Docker
- Python 3.x
- Flask
- SpeechRecognition
- PyAudio (for microphone input, optional)
- Other dependencies listed in `requirements.txt`

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/speech_recognition_app.git
cd speech_recognition_app



#Install dependencies (optional if you're not using Docker)
    pip install -r requirements.txt

#Running the app using Docker
    Build the Docker image:
    docker build -t flask-speech-recognition .

#Run the Docker container:
    docker run -p 5000:5000 flask-speech-recognition

#This will start the Flask app on port 5000.

#Navigate to http://localhost:5000 in your browser to use the app.

#Running the app without Docker (optional)
#If you want to run the app locally without Docker, simply start the Flask app:

    python3 app.py

#And navigate to http://localhost:5000 in your browser.

#Usage
    # 1. Open the application in your browser at http://localhost:5000.
    # 2. Upload an audio file (WAV, MP3, etc.) via the upload form.
    # 3. The app will process the audio and return the text transcribed from the speech.



##########  PROJECT STRUCTURE   ###############

├── Dockerfile
├── README.md
├── app.py
├── requirements.txt
├── speechRecognitionApp
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   └── routes.cpython-311.pyc
│   ├── routes.py
│   ├── static
│   │   └── styles.css
│   ├── templates
│   │   └── index.html
│   └── utils
│       ├── __pycache__
│       │   └── audio_processor.cpython-311.pyc
│       └── audio_processor.py
└── uploads