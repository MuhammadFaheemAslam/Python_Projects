import speech_recognition as sr
from pydub import AudioSegment
from flask import flash

def convert_to_wav(filepath):
    try:
        audio = AudioSegment.from_file(filepath)
        wav_path = filepath.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format='wav')
        return wav_path
    except Exception as e:
        raise Exception(f"Error during conversion: {e}")

def process_audio(filepath):
    recognizer = sr.Recognizer()
    try:
        # Convert to WAV if necessary
        if not filepath.endswith('.wav'):
            filepath = convert_to_wav(filepath)

        # Recognize speech
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)
            return transcription
    except sr.UnknownValueError:
        flash("Speech not recognized.", 'danger')
        raise
        #return "Speech not recognized."
    except sr.RequestError:
        flash("API request error.",'danger')
        raise
        #return "API request error."
    except Exception as e:
        flash(str(e),'danger')
        raise Exception(str(e))
