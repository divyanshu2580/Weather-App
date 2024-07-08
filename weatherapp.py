import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox 
from tkinter import * 
from PIL import Image , ImageTk
import requests
import datetime
import joblib
from sklearn.ensemble import RandomForestClassifier
import sklearn  
import os
from dotenv import load_dotenv , dotenv_values
load_dotenv()

key = os.getenv("API_KEY")

root = tk.Tk()
root.title("Weather Wave ")
root.geometry('400x600')

image_path = "images_WA/background.jpg"
image_back = Image.open(image_path)
image_back = image_back.resize((400,600) , Image.LANCZOS)
bg_image = ImageTk.PhotoImage(image_back)

def show_frame(frame):
    frame.tkraise()

container = tk.Frame(root)
container.pack(side="top" , fill="both", expand=True)

home_frame = tk.Frame(container)
weather_frame = tk.Frame(container)
prediction_frame = tk.Frame(container)
forcast_frame = tk.Frame(container)
start_frame = tk.Frame(container)
by_location_frame  = tk.Frame(container)

for frame in (start_frame , home_frame , weather_frame, prediction_frame , forcast_frame ,by_location_frame):
    frame.grid(row=0,column=0 , sticky='nsew')

#home page

background_label = tk.Label(home_frame, image=bg_image)
background_label.pack(fill=tk.BOTH, expand=True,ipadx=5)

home_label = tk.Label(background_label ,text="Weather Wave",font=("Times New Roman" , 20) ,bg="dark slate blue", fg="white")
home_label.pack( side="top",pady=10)

home_nav_frame = tk.Frame(background_label , bg="black")
home_nav_frame.pack(side="top",pady=10)

tk.Button(home_nav_frame , text="Home" ,font=('Times New Roman', 13),border=5,width=13 , bg="black",fg="white",command= lambda: show_frame(home_frame)).pack( side="left",pady=5)

tk.Button(home_nav_frame , text="Back ",font=('Times New Roman', 13) ,border=5,width=13 , bg="black",fg="white", command= lambda: show_frame(start_frame)).pack( side="left", pady=5)

tk.Button(home_nav_frame , text="Exit " ,font=('Times New Roman', 13),border=5,width=12 , bg="black",fg="white",command= lambda: root.destroy()).pack( side="left",pady=5)

home_center_frame = tk.Frame(background_label , bg="black")
home_center_frame.pack(side='top' , pady=10)
image_path1 = "images_WA/app.png"
image1 = Image.open(image_path1)
image1 = image1.resize((160,160) , Image.LANCZOS)
image_app= ImageTk.PhotoImage(image1)

image_app_label = tk.Label(home_center_frame , image=image_app , bg="black")
image_app_label.pack(side="top",expand=True)

home_bottom_frame = tk.Frame(background_label , bg="black")
home_bottom_frame.pack(side="bottom",pady=20)

home_bottom_frame1 = tk.Frame(background_label , bg="black")
home_bottom_frame1.pack(side="bottom")


tk.Button(home_bottom_frame , text="Weather Page " ,font=('Times New Roman', 15),border=5,width=15 , bg="black",fg="white",command= lambda: show_frame(weather_frame)).pack( side="left")

tk.Button(home_bottom_frame , text="Prediction" ,font=('Times New Roman', 15),border=5,width=15 , bg="black",fg="white",command= lambda: show_frame(prediction_frame)).pack( side="left")

tk.Button(home_bottom_frame1 , text="Forcast Weather" ,font=('Times New Roman', 15),border=5,width=15 , bg="black",fg="white",command= lambda: show_frame(forcast_frame)).pack( side="left")

tk.Button(home_bottom_frame1 , text="Weather by Location" ,font=('Times New Roman', 15),border=5,width=15 , bg="black",fg="white",command= lambda: show_frame(by_location_frame)).pack( side="left")

# label = tk.Label(home_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
# label.pack(side="right", fill="both",padx=10)

# Start Page 

image_path2 = "images_WA/start.jpg"
image_back1 = Image.open(image_path2)
image_back1 = image_back1.resize((400,600) , Image.LANCZOS)
bg_image1 = ImageTk.PhotoImage(image_back1)
background_label1 = tk.Label(start_frame, image=bg_image1)
background_label1.pack(fill=tk.BOTH, expand=True)
start_label = tk.Label(background_label1 ,text="Weather Wave",font=("Times New Roman" , 20) ,bg="blue4", fg="white")
start_label.pack( side="top",pady=10)


start_center_frame = tk.Frame(background_label1 , bg="black")
start_center_frame.pack(side='top' , pady=100)

image_app_label2 = tk.Label(start_center_frame , image=image_app , bg="black")
image_app_label2.pack(side="top",expand=True)

start_bottom_frame = tk.Frame(background_label1 , bg="black")
start_bottom_frame.pack(side="bottom",pady=50)

tk.Button(start_bottom_frame , text="START" ,font=('Times New Roman', 15 , "bold"),border=5,width=10 , bg="navy",fg="white",command= lambda: show_frame(home_frame)).pack( side="top")

# label = tk.Label(start_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
# label.pack(side="right", fill="both",padx=10)

def get_weather():

    location = location_entry.get()

    if not location:
        messagebox.showerror("Error", "Please enter a location.")
        return

    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": key, "units": "metric"}

    try:
        response = requests.get(endpoint, params=params)
        weather_data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed to fetch data: {weather_data.get('message', 'Unknown error')}")
            return

        global original_temps
        original_temps = {
            'current': weather_data['main']['temp'] ,
            'feels_like': weather_data['main']['feels_like'] ,
            'min': weather_data['main']['temp_min'] ,
            'max': weather_data['main']['temp_max'] ,
        }

        city = weather_data.get('name', '')
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed'] * 3.6 
        min_temperature = weather_data['main']['temp_min']
        max_temperature = weather_data['main']['temp_max']
        visibility = weather_data.get('visibility', 0) / 1000  

        city_label.config(text=f"Location: {city}")
        weather_description_label.config(text=f"Weather Description: {weather_description}")
        temperature_label.config(text=f"Temperature: {temperature:.2f} °C")
        feels_like_label.config(text=f"Feels Like: {feels_like:.2f} °C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_speed_label.config(text=f"Wind Speed: {wind_speed:.1f} Km/hr")
        min_temperature_label.config(text=f"Min Temp: {min_temperature:.2f} °C")
        max_temperature_label.config(text=f"Max Temp: {max_temperature:.2f} °C")
        visibility_label.config(text=f"Visibility: {visibility:.2f} Kms")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {str(e)}")
    clear_location()


def celcius():
    temperature_label.config(text=f"Temperature: {original_temps['current']:.2f} °C")
    min_temperature_label.config(text=f"Min Temp: {original_temps['min']:.2f} °C")
    max_temperature_label.config(text=f"Max Temp: {original_temps['max']:.2f} °C")
    feels_like_label.config(text=f"Feels Like: {original_temps['feels_like']:.2f} °C")

def farehnite():
    current_temp = (original_temps['current'] * 9/5) + 32
    min_temp = (original_temps['min'] * 9/5) + 32
    max_temp = (original_temps['max'] * 9/5) + 32
    feels_like_temp = (original_temps['feels_like'] * 9/5) + 32

    temperature_label.config(text=f"Temperature: {current_temp:.2f} °F")
    min_temperature_label.config(text=f"Min Temp: {min_temp:.2f} °F")
    max_temperature_label.config(text=f"Max Temp: {max_temp:.2f} °F")
    feels_like_label.config(text=f"Feels Like: {feels_like_temp:.2f} °F")

def get_forcast():
    location = location1_entry.get()
    if not location:
        messagebox.showerror("Error", "Please enter a location.")
        return

    endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": location, "appid": key, "units": "metric"}

    response = requests.get(endpoint, params=params)
    forecast_data = response.json()

    if forecast_data.get("cod") != "200":
        messagebox.showerror("Error", forecast_data.get("message", "Unable to fetch forecast data."))
        return

    forecast_list = forecast_data.get('list', [])
    if len(forecast_list) < 28:
        messagebox.showerror("Error", "Insufficient forecast data available.")
        return

    forecast_info = ""
    for i in range(1, 21*4, 8):
        if i >= len(forecast_list):
            break
        forecast = forecast_list[i]
        dt_txt = forecast['dt_txt']
        date = dt_txt.split()[0]
        temp = forecast['main']['temp']
        feels_like = forecast['main']['feels_like']
        weather_description = forecast['weather'][0]['description']

        forecast_info += (
            f"Date: {date}\n"
            f"Weather: {weather_description}\n"
            f"Avg. Temp: {temp:.2f}°C, Feels Like: {feels_like:.2f}°C\n\n"
            # f"Max Temp: {max_temperature_f:.2f}°C , Min Temp: {min_temperature_f:.2f}°C \n\n"
        )

    forecast_info_label.config(text=forecast_info)
    clear_location()
    
def clear():
    location_entry.delete(0,tk.END)
    city_label.config(text="")
    weather_description_label.config(text="")
    temperature_label.config(text="")
    feels_like_label.config(text="")
    humidity_label.config(text="")
    wind_speed_label.config(text="")
    min_temperature_label.config(text="")
    max_temperature_label.config(text="")
    visibility_label.config(text="")
    forecast_info_label.config(text="")
    location1_entry.delete(0,tk.END)
def clear_location():
    location1_entry.delete(0,tk.END)
    location_entry.delete(0,tk.END)

#forcast page 

image_path5 = "images_WA/forcast.jpg"
image_back5 = Image.open(image_path5)
image_back5 = image_back5.resize((400,600) , Image.LANCZOS)
bg_image5= ImageTk.PhotoImage(image_back5)

background_label5 = tk.Label(forcast_frame, image=bg_image5)
background_label5.pack(fill=tk.BOTH, expand=True)

forcast_label = tk.Label(background_label5 ,text="Forecast Page",font=("Times New Roman" , 20) ,bg="black", fg="white")
forcast_label.pack( side="top",pady=5)

forcast_nav_frame = tk.Frame(background_label5 , bg="black")
forcast_nav_frame.pack(side="top",pady=5)

tk.Button(forcast_nav_frame , text="Home" ,font=('Times New Roman', 13),border=5,width=13 , bg="black",fg="white",command= lambda: show_frame(home_frame)).pack( side="left",pady=5)

tk.Button(forcast_nav_frame , text="Clear ",font=('Times New Roman', 13) ,border=5,width=13 , bg="black",fg="white", command= clear).pack( side="left", pady=5)

tk.Button(forcast_nav_frame , text="Exit " ,font=('Times New Roman', 13),border=5,width=12 , bg="black",fg="white",command= lambda: root.destroy()).pack( side="left",pady=5)

forcast_center_frame = tk.Frame(background_label5 , bg="black")
forcast_center_frame.pack(side='top' , pady=5)

forecast_info_label= tk.Label(forcast_center_frame, font=("Times New Roman", 11), bg="black", fg="white")
forecast_info_label.pack(pady=3)

forcast_bottom_frame = tk.Frame(background_label5 , bg="black")
forcast_bottom_frame.pack(side="bottom",pady=5)

location1_label = tk.Label(forcast_bottom_frame, text="Enter Location ",bg='black', fg='white',font=('Times New Roman', 15,'bold'))
location1_label.pack( side="left")

location1_entry = tk.Entry(forcast_bottom_frame, bg='white',font=('Times New Roman', 15,'bold'),border=5)
location1_entry.pack(ipady=5,padx=5,pady=5)

buttons_frame_forcast = tk.Frame(background_label5 )
buttons_frame_forcast.pack(side="bottom")

tk.Button(buttons_frame_forcast, text="Forecast Weather " ,font=('Times New Roman', 13),border=5,width=15 , bg="black",fg="white",command= get_forcast).pack( side="left")

# label = tk.Label(forcast_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
# label.pack(side="right", fill="both",padx=10)


# weather page 

image_path3 = "images_WA/weather.jpg"
image_back2 = Image.open(image_path3)
image_back2 = image_back2.resize((400,600) , Image.LANCZOS)
bg_image2= ImageTk.PhotoImage(image_back2)

background_label2 = tk.Label(weather_frame, image=bg_image2)
background_label2.pack(fill=tk.BOTH, expand=True)

home_label = tk.Label(background_label2 ,text="Weather Page",font=("Times New Roman" , 20) ,bg="midnight blue", fg="white")
home_label.pack( side="top",pady=5)

weather_nav_frame = tk.Frame(background_label2 , bg="black")
weather_nav_frame.pack(side="top",pady=5)

tk.Button(weather_nav_frame , text="Home" ,font=('Times New Roman', 13),border=5,width=13 , bg="black",fg="white",command= lambda: show_frame(home_frame)).pack( side="left",pady=5)

tk.Button(weather_nav_frame , text="Clear ",font=('Times New Roman', 13) ,border=5,width=13 , bg="black",fg="white", command= clear).pack( side="left", pady=5)

tk.Button(weather_nav_frame , text="Exit " ,font=('Times New Roman', 13),border=5,width=12 , bg="black",fg="white",command= lambda: root.destroy()).pack( side="left",pady=5)

weather_center_frame = tk.Frame(background_label2 , bg="midnight blue")
weather_center_frame.pack(side='top' , pady=10)

city_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
city_label.pack(pady=1)
weather_description_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
weather_description_label.pack(pady=1)
temperature_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
temperature_label.pack(pady=1)
feels_like_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
feels_like_label.pack(pady=1)
humidity_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
humidity_label.pack(pady=1)
wind_speed_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
wind_speed_label.pack(pady=1)
min_temperature_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
min_temperature_label.pack(pady=1)
max_temperature_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
max_temperature_label.pack(pady=1)
visibility_label = tk.Label(weather_center_frame, text="", font=("Times New Roman", 13), bg="midnight blue", fg="white")
visibility_label.pack(pady=1)

weather_bottom_frame = tk.Frame(background_label2 , bg="black")
weather_bottom_frame.pack(side="bottom",pady=10)

location_label = tk.Label(weather_bottom_frame, text="Enter Location ",bg='black', fg='white',font=('Times New Roman', 15,'bold'))
location_label.pack( side="left")

location_entry = tk.Entry(weather_bottom_frame, bg='white',font=('Times New Roman', 15,'bold'),border=5)
location_entry.pack(ipady=5,padx=5,pady=5)

buttons_frame_weather = tk.Frame(background_label2 )
buttons_frame_weather.pack(side="bottom")

tk.Button(buttons_frame_weather, text="Celcius" ,font=('Times New Roman', 13),border=5,width=7 , bg="black",fg="white",command= celcius).pack( side="left",padx=5,pady=5)

tk.Button(buttons_frame_weather, text="Get the Weather" ,font=('Times New Roman', 13),border=5,width=15 , bg="black",fg="white",command= get_weather).pack( side="left",padx=5,pady=5)

tk.Button(buttons_frame_weather, text="Farenheit" ,font=('Times New Roman', 13),border=5,width=7 , bg="black",fg="white",command= farehnite).pack( side="left",padx=5,pady=5)

# label = tk.Label(weather_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
# label.pack(side="right", fill="both",padx=10)

# prediction page 

def predict_weather():
    try:
        temp_pred = float(temp_entry.get())
        feels_pred = float(feels_like_entry.get())
        air_pred = float(air_qual_entry.get())
        humid_pred = float(humidity_entry.get())
        precip_pred = float(precip_entry.get())
        visible_pred = float(visibility_entry.get())
        wind_pred = float(wind_speed_entry.get())
        press_pred = float(pressure_entry.get())
        
        input_data = [[temp_pred, feels_pred, air_pred, humid_pred, precip_pred, visible_pred, wind_pred, press_pred]]
        
        prediction_model = "model.pkl"
        model = joblib.load(prediction_model)
        prediction = model.predict(input_data)
        
        result_label.config(text=f"Prediction: {prediction[0]}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

image_path4 = "images_WA/prediction.jpg"
image_back4 = Image.open(image_path4)
image_back4 = image_back4.resize((400,600) , Image.LANCZOS)
bg_image4= ImageTk.PhotoImage(image_back4)

background_label4 = tk.Label(prediction_frame, image=bg_image4)
background_label4.pack(fill=tk.BOTH, expand=True)

weather_pred_label = tk.Label(background_label4 ,text="Weather Prediction Page",font=("Times New Roman" , 20) ,bg="black", fg="white")
weather_pred_label.pack( side="top",pady=5)

prediction_nav_frame = tk.Frame(background_label4 , bg="black")
prediction_nav_frame.pack(side="top",pady=5)

tk.Button(prediction_nav_frame , text="Home" ,font=('Times New Roman', 13),border=5,width=13 , bg="black",fg="white",command= lambda: show_frame(home_frame)).pack( side="left",pady=5)

tk.Button(prediction_nav_frame , text="Clear ",font=('Times New Roman', 13) ,border=5,width=13 , bg="black",fg="white", command= lambda: show_frame(start_frame)).pack( side="left", pady=5)

tk.Button(prediction_nav_frame , text="Exit " ,font=('Times New Roman', 13),border=5,width=12 , bg="black",fg="white",command= lambda: root.destroy()).pack( side="left",pady=5)

prediction_center_frame = tk.Frame(background_label4 , bg="black")
prediction_center_frame.pack(side='top' , pady=5)

exapmle_label = tk.Label(prediction_center_frame,text="Example   -  20°C    -     23°C    -    203    -    70%" , fg="white" , bg="black",font=("Times New Roman" , 13))
exapmle_label.pack()
exapmle_label1 = tk.Label(prediction_center_frame,text="    0.001mm    -  7.00km   -   5.4km/h   -   1007mb    ", fg="white" , bg="black",font=("Times New Roman" , 13))
exapmle_label1.pack()

temprature_frame = tk.Frame(background_label4 ,bg="black")
temprature_frame.pack(side='top' ,ipady=2 )

temp_entry_label = tk.Label(temprature_frame ,text="  Enter temprature  °C   ",font=("Times New Roman" , 13) ,bg="black", fg="white")
temp_entry_label.pack( side="left")
temp_entry = tk.Entry(temprature_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
temp_entry.pack(side="right")

feels_frame = tk.Frame(background_label4 ,bg="black")
feels_frame.pack(side='top' ,ipady=2)

feels_entry_label = tk.Label(feels_frame ,text="   Enter Feels like  °C    ",font=("Times New Roman" , 13) ,bg="black", fg="white")
feels_entry_label.pack( side="left")
feels_like_entry = tk.Entry(feels_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
feels_like_entry.pack(side="right")

air_frame = tk.Frame(background_label4 ,bg="black")
air_frame.pack(side='top' ,ipady=2)

air_entry_label = tk.Label(air_frame ,text="     Enter Air  Quality     ",font=("Times New Roman" , 13) ,bg="black", fg="white")
air_entry_label.pack(side="left" )
air_qual_entry = tk.Entry(air_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
air_qual_entry.pack(side="right")

humidity_frame = tk.Frame(background_label4 ,bg="black")
humidity_frame.pack(side='top',ipady=2)

humidity_entry_label = tk.Label(humidity_frame ,text="     Enter Humidity   %   ", font=("Times New Roman" , 13) ,bg="black", fg="white")
humidity_entry_label.pack( side="left")
humidity_entry = tk.Entry(humidity_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
humidity_entry.pack(side="right")

precip_frame = tk.Frame(background_label4 ,bg="black")
precip_frame.pack(side='top' ,ipady=2)

precip_entry_label = tk.Label(precip_frame ,text="Enter Precipitation mm ",font=("Times New Roman" , 13) ,bg="black", fg="white")
precip_entry_label.pack( side="left")
precip_entry = tk.Entry(precip_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
precip_entry.pack(side="right")

visibility_frame = tk.Frame(background_label4 ,bg="black")
visibility_frame.pack(side='top',ipady=2)

visibility_entry_label = tk.Label(visibility_frame ,text="    Enter Visibility  Km   ",font=("Times New Roman" , 13) ,bg="black", fg="white")
visibility_entry_label.pack( side="left")
visibility_entry = tk.Entry(visibility_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
visibility_entry.pack(side="right")

wind_frame = tk.Frame(background_label4 ,bg="black")
wind_frame.pack(side='top' ,ipady=2)

wind_entry_label = tk.Label(wind_frame ,text="Enter Wind Speed  km/h",font=("Times New Roman" , 13) ,bg="black", fg="white")
wind_entry_label.pack(side="left" )
wind_speed_entry = tk.Entry(wind_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
wind_speed_entry.pack(side="right")

pressure_frame = tk.Frame(background_label4 ,bg="black")
pressure_frame.pack(side='top' ,ipady=2)

pressure_entry_label = tk.Label(pressure_frame ,text="     Enter  Pressure   mb  ",font=("Times New Roman" , 13) ,bg="black", fg="white")
pressure_entry_label.pack(side="left" )
pressure_entry = tk.Entry(pressure_frame, bg='white',font=('Times New Roman', 13,'bold'),border=5)
pressure_entry.pack(side="right")

prediction_button_frame = tk.Frame(background_label4 , bg="black")
prediction_button_frame.pack(side="top",pady=5)

tk.Button(prediction_button_frame, text="Predict the Weather" ,font=('Times New Roman', 13),border=5,width=15 , bg="black",fg="white",command= predict_weather  ).pack( )

prediction_bottom_frame = tk.Frame(background_label4 , bg="black")
prediction_bottom_frame.pack(side="bottom",pady=20)

result_label = tk.Label(prediction_bottom_frame,text="", font=("Times New Roman", 15), bg="black", fg="white" )
result_label.pack(side="top",ipadx=5, ipady=5)

# label = tk.Label(prediction_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
# label.pack(side="right", fill="both",padx=10)

# by location page 

def update_cities(*args):
    selected_country = country_var.get()
    cities = country_city_map.get(selected_country, [])
    city_var.set('')
    city_menu['menu'].delete(0, 'end')
    
    for city in cities:
        city_menu['menu'].add_command(label=city, command=tk._setit(city_var, city))

def weather_by_location():
    selected_city = city_var.get()
    if not selected_city:
        messagebox.showerror("Error", "Please Select a city.")
        return

    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    api_key = key
    params = {"q": selected_city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(endpoint, params=params)
        location_data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed to fetch weather data: {location_data.get('message', 'Unknown Error')}")
            return

        temp = location_data['main']['temp']
        feels_like = location_data['main']['feels_like']
        weather_description = location_data['weather'][0]['description']
        humidity = location_data['main']['humidity']
        wind_speed = location_data['wind']['speed'] * 3.6 
        min_temperature = location_data['main']['temp_min']
        max_temperature = location_data['main']['temp_max']
        visibility = location_data.get('visibility', 0) / 1000
        

        location_info_label.config(text=f"Weather: {weather_description}\n"
                                        f"Temperature: {temp:.2f}°C\n"
                                        f"Feels Like: {feels_like:.2f}°C\n"
                                        f"Humidity: {humidity:.2f}%\n"
                                        f"Wind Speed: {wind_speed:.2f}\n"
                                        f"Min Temperature: {min_temperature}°C\n"
                                        f"Max Temperature: {max_temperature}°C\n"
                                        f"Visibility: {visibility}km\n"
                                        )

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")    

image_path6 = "images_WA/location.jpg"
image_back6 = Image.open(image_path6)
image_back6 = image_back6.resize((400,600) , Image.LANCZOS)
bg_image6= ImageTk.PhotoImage(image_back6)

background_label6 = tk.Label(by_location_frame, image=bg_image6)
background_label6.pack(fill=tk.BOTH, expand=True)

by_location_label = tk.Label(background_label6 ,text="Weather Prediction Page",font=("Times New Roman" , 20) ,bg="black", fg="white")
by_location_label.pack( side="top",pady=5)

location_nav_frame = tk.Frame(background_label6 , bg="black")
location_nav_frame.pack(side="top",pady=15)

tk.Button(location_nav_frame , text="Home" ,font=('Times New Roman', 13),border=5,width=13 , bg="black",fg="white",command= lambda: show_frame(home_frame)).pack( side="left",pady=5)

tk.Button(location_nav_frame , text="Clear ",font=('Times New Roman', 13) ,border=5,width=13 , bg="black",fg="white", command= lambda: show_frame(start_frame)).pack( side="left", pady=5)

tk.Button(location_nav_frame , text="Exit " ,font=('Times New Roman', 13),border=5,width=12 , bg="black",fg="white",command= lambda: root.destroy()).pack( side="left",pady=5)

option_country_frame = tk.Frame(background_label6 , bg="black")
option_country_frame.pack(side="top")

option_city_frame = tk.Frame(background_label6 , bg="black")
option_city_frame.pack(side="top")

country_city_map = {
    "India": ["Delhi", "Mumbai", "Bangalore", "Chennai","Jaipur"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston","Alaska"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Ottawa","Victoria"],
    "UK":['London','Wales','Derby','Chester','Manchester']
}

menu_font = ('Times New Roman', 13)
menu_bg = 'black'
menu_fg = 'white'

country_var = tk.StringVar()
city_var = tk.StringVar()

tk.Label(option_country_frame, text="              Select  Country             ", bg="black",fg="white",font=('Times New Roman', 13)).pack(pady=5)
country_menu = tk.OptionMenu(option_country_frame, country_var, *country_city_map.keys())
country_menu.pack(pady=5)
country_var.set("Select a counrty")

tk.Label(option_city_frame, text="                 Select  City                 ", bg="black",fg="white",font=('Times New Roman', 13)).pack(pady=5)
city_menu = tk.OptionMenu(option_city_frame, city_var, '')
city_menu.pack(pady=5)
city_var.set("Select a city")

country_var.trace('w', update_cities)

country_menu['menu'].config(bg=menu_bg, fg=menu_fg)
country_menu.config(bg=menu_bg, fg=menu_fg, font=menu_font, indicatoron=0)

city_menu['menu'].config(bg=menu_bg, fg=menu_fg)
city_menu.config(bg=menu_bg, fg=menu_fg, font=menu_font, indicatoron=0)

location_button_frame = tk.Frame(background_label6 , bg="black")
location_button_frame.pack(side="top",pady=10)

tk.Button(location_button_frame, text="Predict the Weather" ,font=('Times New Roman', 13),border=5,width=15 , bg="black",fg="white",command= weather_by_location).pack( )

location_info_label= tk.Label(background_label6, font=("Times New Roman", 13), bg="black", fg="white")
location_info_label.pack(pady=5)

show_frame(start_frame)
root.mainloop()