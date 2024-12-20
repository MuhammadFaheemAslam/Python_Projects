from flask import Flask
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'e63c17ca4336b639998adba2f696686b'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Register blueprints (optional)
from .routes import main
app.register_blueprint(main)
    


