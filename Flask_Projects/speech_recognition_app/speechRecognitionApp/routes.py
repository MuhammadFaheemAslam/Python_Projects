from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from speechRecognitionApp import app
from .utils.audio_processor import process_audio

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET', 'POST'])
def index():
    transcription = None
    if request.method == 'POST':
        # Check if file is in request
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process audio
            transcription = process_audio(filepath)
            flash('Audio processed successfully!','success')
        else:
            flash('Invalid file format')

    return render_template('index.html', transcription=transcription)
