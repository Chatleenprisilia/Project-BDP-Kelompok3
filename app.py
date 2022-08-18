from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

daftarDaerah = {
    "Sulawesi Utara" : ["Bitung", "Kotamobagu", "Manado" , "Tomohon" ]
}

# Untuk sementara ganti2 disini dulu depe nama kota
def get_loc(kota = "Manado"):
    response = requests.get("https://api.openweathermap.org/geo/1.0/direct?q="+kota+",ID&appid=e54dbc2098b0353a98133dbdf262e83c")
    parse_json = json.loads(response.text)
    lat = parse_json[0]['lat']
    lon = parse_json[0]['lon']
    return kota, lat, lon

def get_weather(lat,lon):
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&units=metric&appid=e54dbc2098b0353a98133dbdf262e83c&lang=id")
    parse_json = json.loads(response.text)
    temp = parse_json['main']['temp']
    humid = parse_json['main']['humidity']
    press = parse_json['main']['pressure']
    windspd = parse_json['wind']['speed']
    if "rain" in parse_json:
        rain = parse_json['rain']
    else:
        rain=0
    desc = parse_json['weather'][0]['description']
    return temp, humid, press, windspd, rain, desc



@app.route("/")
def main(methods=["POST","GET"]):
    dataKota = get_loc()
    dataCuaca = get_weather(str(dataKota[1]), str(dataKota[2]))

    return render_template('index.html', kota=dataKota, cuaca=dataCuaca)

""""
@app.route("/<cty>")
def city(cty):
    dataKota = get_loc(cty)
    dataCuaca = get_weather(str(dataKota[1]), str(dataKota[2]))
    return render_template('index.html', kota=dataKota, cuaca=dataCuaca)
"""

if __name__ == "__main__":
    app.run()