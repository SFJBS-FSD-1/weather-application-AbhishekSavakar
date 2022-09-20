import requests
from flask import Flask, render_template, request
import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form["city"]
        api = "997ea79e1c9575bd4f087cf90e68205d"
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + city + "/<START_DATE>/<END_DATE>?key=<YOUR_API_KEY>"
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api + "&units=metric"
        print(url)
        response = requests.get(url).json()
        print(response)

        if response['cod'] == 200:
            data = {"temp": response["main"]["temp"], "lon": response["coord"]["lon"], "lat": response["coord"]["lat"],
                    "name": response["name"],
                    "sunrise": datetime.datetime.fromtimestamp(response.get('sys')['sunrise']),
                    "sunset": datetime.datetime.fromtimestamp(response.get('sys')['sunset']), "code": response["cod"],
                    }
            return render_template('home.html', data=data)
        elif response["cod"] == "404":
            data = {"message": response['message'], "code": int(response["cod"])}
            return render_template('home.html', data=data)
    else:
        data = None
        return render_template('home.html', data=data)

# Creating port
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(port=port)
