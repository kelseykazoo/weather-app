import tkinter as tk
import requests
from config import API_KEY


def get_weather_emoji(description):
    desc = description.lower()
    if "clear" in desc:
        return "☀️"
    elif "cloud" in desc:
        return "☁️"
    elif "rain" in desc:
        return "🌧️"
    elif "storm" in desc or "thunder" in desc:
        return "⛈️"
    elif "snow" in desc:
        return "❄️"
    elif "mist" in desc or "fog" in desc:
        return "🌫️"
    elif "drizzle" in desc:
        return "🌦️"
    else:
        return "🌈"


def on_entry_click(event):
    if entry.get() == "Enter your city":
        entry.delete(0, tk.END)
        entry.config(fg="#023047")


def on_focusout(event):
    if entry.get() == "":
        entry.insert(0, "Enter your city")
        entry.config(fg="gray")


def submitForm():
    city = username.get().strip()

    if not city or city.lower() == "enter your city":
        result_label.config(text="Please enter a valid city name.")
        return

    
    city = " ".join(word.capitalize() for word in city.split())

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            result_label.config(text="City not found.")
            return

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"].title()
        emoji = get_weather_emoji(weather)

        result_label.config(text=f"{emoji} {city}: {temp}°F, {weather}")

    except Exception as e:
        result_label.config(text="Error getting weather data.")
        print(e)


root = tk.Tk()
root.title("Weather App 🌞")
root.configure(bg="#023047")
root.geometry("300x300")


tk.Label(
    root,
    text="Weather App 🌞",
    font=("Helvetica", 20, "bold"),
    bg="#023047",
    fg="#219ebc"
).pack(pady=10)


username = tk.StringVar()
entry = tk.Entry(
    root,
    textvariable=username,
    font=("Helvetica", 12),
    bg="#219ebc",
    fg="gray",
    justify='center'
)
entry.insert(0, "Enter your city")
entry.pack(pady=10, ipadx=10, ipady=4)


entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focusout)


result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 12, "bold"),
    bg="#023047",
    fg="#219ebc",
    justify='center'
)
result_label.pack(pady=10)

check_button = tk.Button(
    root,
    text="Check Weather",
    command=submitForm,
    font=("Helvetica", 12, "bold"),
    bg="#219ebc",
    fg="#023047",
    activebackground="#8ecae6",
    activeforeground="#023047",
    relief="flat",
    bd=0,
    padx=10,
    pady=5
)
check_button.pack()

root.mainloop()
