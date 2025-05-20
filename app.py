from tkinter import *
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from datetime import datetime
import webbrowser
import os
from dotenv import load_dotenv
load_dotenv()




# Initialize the main window
root = Tk()
root.title("Weather App")
root.geometry("750x500")
root.resizable(False, False)

# Load background image
bg_image = Image.open("background.jpg")  # Replace with your image
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover the full window

# Function to fetch weather details
def get_weather():
    city = city_input.get()
    api_key = os.getenv("api_key")
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp'] - 273.15  # Convert to Celsius
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed'] * 3.6  # Convert to km/h
        description = data['weather'][0]['description']
        cloudy = data['clouds']['all']
        epoch_time = data['dt']
        date_time = datetime.fromtimestamp(epoch_time)

        # Update labels with fetched data
        timelabel.config(text=f"Updated: {date_time.strftime('%Y-%m-%d %H:%M:%S')}")
        temp_label.config(text=f"{temp:.2f}°C")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind: {wind:.2f} km/h")
        cloud_label.config(text=f"Cloud: {cloudy}%")
        desc_label.config(text=description.capitalize())

        # Load corresponding weather icon
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, stream=True)
        if icon_response.status_code == 200:
            img_data = Image.open(icon_response.raw)
            img_data = img_data.resize((100, 100), Image.Resampling.LANCZOS)
            weather_icon = ImageTk.PhotoImage(img_data)
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon

    else:
        messagebox.showerror("Error", "City not found!")
        city_input.delete(0, END)

# Function to open detailed forecast
def get_forecast():
    city = city_input.get()
    url = f'https://wttr.in/{city}'
    webbrowser.open(url)

# Function to reset the input and labels
def reset():
    city_input.delete(0, END)
    timelabel.config(text="")
    temp_label.config(text="--°C")
    pressure_label.config(text="-- hPa")
    humidity_label.config(text="--%")
    wind_label.config(text="-- km/h")
    cloud_label.config(text="--%")
    desc_label.config(text="--")
    icon_label.config(image="")

# Styling
style = ttk.Style()
style.configure('TButton', font=('Arial', 12, 'bold'), background='#28a745', foreground='white', padding=5)

# UI Layout
title = Label(root, text='WeatherNow', font=("Verdana", 18, "bold"), fg='brown', bg='lightblue1')
title.pack(pady=10)

frame = Frame(root, bg="white", bd=5)
frame.pack(pady=10)

Label(frame, text='Enter city name:', font=('Arial', 12,'bold'), bg='white').grid(row=0, column=0, padx=10, pady=5)
city_input = ttk.Entry(frame, font=('Arial', 12), width=20)
city_input.grid(row=0, column=1, padx=10, pady=5)


style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), foreground="black", background="lightblue")

btn_submit = ttk.Button(frame, text='Get Weather',style="TButton",command=get_weather)
btn_submit.grid(row=0, column=2, padx=10, pady=5)

btn_forecast = ttk.Button(frame, text='Forecast',style="TButton",command=get_forecast)
btn_forecast.grid(row=0, column=3, padx=10, pady=5)

btn_reset = ttk.Button(frame, text='Reset',style="TButton", command=reset)
btn_reset.grid(row=0, column=4, padx=10, pady=5)

# Weather Display Frame
weather_frame = Frame(root, bg="lightblue", bd=3)
weather_frame.pack(pady=20, fill="both", expand=True)

timelabel = Label(weather_frame, text="", font=("Arial", 10), bg="lightblue")
timelabel.pack(pady=5)

icon_label = Label(weather_frame, bg="lightblue")  # Weather Icon
icon_label.pack(pady=5)

temp_label = Label(weather_frame, text="--°C", font=("Arial", 20, "bold"), bg="lightblue", fg="red")
temp_label.pack()

desc_label = Label(weather_frame, text="--", font=("Arial", 14), bg="lightblue")
desc_label.pack()

pressure_label = Label(weather_frame, text="-- hPa", font=("Arial", 12), bg="lightblue")
pressure_label.pack()

humidity_label = Label(weather_frame, text="--%", font=("Arial", 12), bg="lightblue")
humidity_label.pack()

wind_label = Label(weather_frame, text="-- km/h", font=("Arial", 12), bg="lightblue")
wind_label.pack()

cloud_label = Label(weather_frame, text="--%", font=("Arial", 12), bg="lightblue")
cloud_label.pack()

# Run the app
root.mainloop()
