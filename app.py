from flask import Flask, render_template, request
import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")


app = Flask(__name__)


def get_weather_emoji(description):
    if "cloud" in description.lower():
        return "☁️"
    elif "sun" in description.lower() or "clear" in description.lower():
        return "☀️"
    elif "rain" in description.lower():
        return "🌧️"
    elif "storm" in description.lower() or "thunder" in description.lower():
        return "⛈️"
    elif "snow" in description.lower():
        return "❄️"
    elif "fog" in description.lower() or "mist" in description.lower():
        return "🌫️"
    else:
        return "🌈"


def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return None, None, None, None, "default"

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"].title()
        emoji = get_weather_emoji(weather)
        icon = data["weather"][0]["icon"]

        description = data["weather"][0]["description"].lower()

        if "cloud" in description:
            weather_class = "clouds"
        elif "rain" in description:
            weather_class = "rain"
        elif "mist" in description:
            weather_class = "mist"
        elif "snow" in description:
            weather_class = "snow"
        elif "clear" in description:
            weather_class = "sunny"
        else:
            weather_class = "default"

        return temp, weather, emoji, icon, weather_class

    except Exception as e:
        print("Error:", e)
        return None, None, None, None, "default"


@app.route("/", methods=["GET", "POST"])
def home():
    city = "Corpus Christi"
    if request.method == "POST":
        city = request.form.get("city")

    temp, weather, emoji, icon, weather_class = get_weather_data(city)

    return render_template(
        "index.html",
        city=city,
        temp=temp,
        weather=weather,
        emoji=emoji,
        icon=icon,
        weather_class=weather_class,
    )


@app.route("/autoweather")
def autoweather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    geo_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"
    try:
        response = requests.get(geo_url)
        data = response.json()
        city = data[0]["name"]
        return {"city": city}
    except:
        return {"city": None}
