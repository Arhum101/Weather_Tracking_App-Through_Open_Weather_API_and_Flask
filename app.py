import os
from flask import Flask, render_template,request
import requests
from dotenv import load_dotenv
import datetime 

load_dotenv() 
app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/', methods=["GET", "POST"])
def index():
    weather_data = None
    error_msg = None 

    if request.method == "POST":
        city = request.form.get("city")
        if city: 
            base_url = "https://api.openweathermap.org/data/2.5/weather"
            query_params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            
            try:
                response = requests.get(base_url, params=query_params)
                
                if response.status_code == 200:
                    weather_data = response.json()
                elif response.status_code == 401:
                    error_msg = "Invalid API Key. Please double check your .env file."
                elif response.status_code == 404:
                    error_msg = f"City '{city}' not found. Please check spelling."
                else:
                    error_msg = f"Server returned error code: {response.status_code}"
                    
            except Exception as e:
                error_msg = f"An unexpected error occurred: {str(e)}"

    return render_template("index.html", weather=weather_data, error=error_msg, time=datetime.now())

if __name__ == "__main__":
    app.run(debug=True)