# import os
# import requests
# from dotenv import load_dotenv
# from datetime import datetime

# from flask import Flask, render_template, request

# app = Flask(__name__)

# load_dotenv()
# user_api = os.getenv('current_weather_data')

# # user_api = os.environ['current_weather_data']
# location = input("Enter the location (city name): ")

# complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+user_api

# response = requests.get(complete_api_link)
# api_data = response.json()

# #print(api_data)
# @app.route('/',methods=['GET', 'POST'])
# def check_weather():
#     if api_data['cod'] == '404':
#         print("Invalid city: {}, please check your city name".format(location))
#     else:
#         temp_city = ((api_data['main']['temp'])-273.15)
#         weather_desc = api_data['weather'][0]['description']
#         hmdt = api_data['main']['humidity']
#         wind_spd = api_data['wind']['speed']
#         date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
        
#         print("-------------------------------------------------------------")
#         print("Weather Stats for - {} || {}".format(location.upper(), date_time))
#         print("-------------------------------------------------------------")
#         print("Current temperature is: {:.2f} deg C".format(temp_city))
#         print("Current weather desc  :", weather_desc)
#         print("Current Humidity      :", hmdt, '%')
#         print("Current wind speed    :", wind_spd, 'km/h')

import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv('current_weather_data')

@app.route("/", methods=["GET", "POST"])
def check_weather():
    weather = None
    forecast = []
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        # Current weather API
        current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        current_response = requests.get(current_url).json()
        forecast_response = requests.get(forecast_url).json()

        if current_response.get("cod") != 200:
            error = f"City '{city}' not found."
        else:
            weather = {
                "city": city.title(),
                "temp": current_response["main"]["temp"],
                "description": current_response["weather"][0]["description"],
                "humidity": current_response["main"]["humidity"],
                "wind_speed": current_response["wind"]["speed"],
                "datetime": datetime.now().strftime("%d %b %Y | %I:%M %p")
            }

            # Extract 5 days (every 24 hrs at 12:00)
            for item in forecast_response["list"]:
                if "12:00:00" in item["dt_txt"]:
                    forecast.append({
                        "date": item["dt_txt"].split(" ")[0],
                        "temp": item["main"]["temp"],
                        "description": item["weather"][0]["description"],
                        "icon": item["weather"][0]["icon"]
                    })

    return render_template("index.html", weather=weather, forecast=forecast, error=error)


# @app.route("/", methods=["GET", "POST"])
# def check_weather():
#     weather = None
#     error = None

#     if request.method == "POST":
#         location = request.form.get("city")

#         url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
#         response = requests.get(url)
#         api_data = response.json()

#         if api_data.get("cod") != 200:
#             error = f"City '{location}' not found. Please check the spelling."
#         else:
#             weather = {
#                 "city": location.title(),
#                 "temp": api_data["main"]["temp"],
#                 "description": api_data["weather"][0]["description"],
#                 "humidity": api_data["main"]["humidity"],
#                 "wind_speed": api_data["wind"]["speed"],
#                 "datetime": datetime.now().strftime("%d %b %Y | %I:%M %p")
#             }

#     return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
