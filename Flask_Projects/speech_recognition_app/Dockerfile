FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    flac \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
