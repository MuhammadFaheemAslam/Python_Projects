from flask import Flask, request, render_template
import os, requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

@dataclass
class WeatherData:
    name: str
    country: str
    temperature: float
    feels_like: float
    description: str
    emoji: str
    humidity: int
    wind_speed: int
    local_time: str
    time_of_day: str

def get_weather_emoji(description, time_of_day):
    """Return an emoji based on the weather description and time of day."""
    if "clear" in description:
        if time_of_day == "Morning":
            return "🌅"  # Sunrise
        elif time_of_day == "Afternoon":
            return "🌞"  # Bright Sun
        elif time_of_day == "Evening":
            return "🌇"  # Sunset
        else:
            return "🌙"  # Moon (Night)
    elif "cloud" in description:
        return "☁️"  # Cloud
    elif "rain" in description:
        return "🌧️"  # Rain
    elif "snow" in description:
        return "❄️"  # Snow
    elif "thunderstorm" in description:
        return "⛈️"  # Thunderstorm
    elif "fog" in description or "smoke" in description or "mist" in description:
        return "🌫️"  # Fog/Mist
    else:
        return "🌈"  # Default

def process_weather_data(jsonData):
    """Process the JSON data from the weather API and return a WeatherData object."""
    name = jsonData['name']
    country = jsonData['sys']['country']
    temperature = jsonData['main']['temp']
    feels_like = jsonData['main']['feels_like']
    description = jsonData['weather'][0]['description']
    humidity = jsonData['main']['humidity']
    wind_speed = jsonData['wind']['speed']
    timezone_offset = jsonData['timezone']

    # Calculate the local time
    utc_now = datetime.utcnow()
    local_time = utc_now + timedelta(seconds=timezone_offset)
    local_time_formatted = local_time.strftime('%Y-%m-%d %I:%M %p')  # Format time

    # Determine time of day
    hour = local_time.hour
    if hour >= 0 and hour < 6:
        time_of_day = "Night"
    elif hour >= 6 and hour < 12:
        time_of_day = "Morning"
    elif hour >= 12 and hour < 18:
        time_of_day = "Afternoon"
    elif hour >= 18 and hour < 21:
        time_of_day = "Evening"
    else:
        time_of_day = "Late Night"

    # Get emoji based on weather description and time of day
    emoji = get_weather_emoji(description, time_of_day)

    return WeatherData(
        name=name,
        country=country,
        temperature=temperature,
        feels_like=feels_like,
        description=description,
        emoji=emoji,
        humidity=humidity,
        wind_speed=wind_speed,
        local_time=local_time_formatted,
        time_of_day=time_of_day
    )

@app.route("/", methods=['GET', 'POST'])
def home():
    weather_data = None
    if request.method == 'POST':
        city_name = request.form.get("city_name")
        if city_name:
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
            resp = requests.get(weather_url).json()
            
            if resp['cod'] == 200:
                weather_data = process_weather_data(resp)
                print(weather_data)
            else:
                weather_data = {"error": "City not found or city incorrect"}

    return render_template("index.html", weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
