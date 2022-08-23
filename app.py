from flask import Flask, render_template, request
from tkinter import *
from tkinter import ttk
import requests
import json

daftarDaerah = {
    "Aceh" : ["Banda Aceh", "Langsa", "Lhokseumawe" , "Sabang", "Subulussalam"],
    "Bali" : ["Denpasar"],
    "Bangka Belitung" : ["Pangkalpinang"],
    "Banten" : ["Cilegon", "Serang", "Tangerang Selatan" , "Tangerang"],
    "Bengkulu" : ["Bengkulu"],
    "Daerah Istimewa Yogyakarta" : ["Yogyakarta"],
    "Gorontalo" : ["Gorontalo"],
    "Daerah Khusus Ibukota Jakarta" : ["Jakarta"],
    "Jambi" : ["Sungai Penuh", "Jambi"],
    "Jawa Barat" : ["Bandung", "Bekasi", "Bogor", "Cimahi", "Cirebon", "Depok", "Sukabumi", "Tasikmalaya", "Banjar"],
    "Jawa Tengah" : ["Magelang", "Pekalongan", "Salatiga", "Semarang", "Surakarta", "Tegal"],
    "Jawa Timur" : ["Batu", "Blitar", "Kediri", "Madiun", "Malang", "Mojokerto", "Pasuruan", "Probolinggo", "Surabaya"],
    "Kalimantan Barat" : ["Pontianak", "Singkawang"],
    "Kalimantan Selatan" : ["Banjarbaru", "Banjarmasin"],
    "Kalimantan Tengah" : ["Palangka Raya"],
    "Kalimantan Timur" : ["Balikpapan", "Bontang", "Samarinda"],
    "Kalimantan Utara" : ["Tarakan"],
    "Kepulauan Riau" : ["Batam", "Tanjung Pinang"],
    "Lampung" : ["Bandar Lampung", "Metro"],
    "Maluku Utara" : ["Ternate", "Tidore Kepulauan"],
    "Maluku" : ["Ambon", "Tual"],
    "Nusa Tenggara Barat" : ["Bima", "Mataram"],
    "Nusa Tenggara Timur" : ["Kupang"],
    "Papua Barat" : ["Sorong"],
    "Papua" : ["Jayapura"],
    "Riau" : ["Dumai", "Pekanbaru"],
    "Sulawesi Selatan" : ["Makassar", "Palopo", "Parepare"],
    "Sulawesi Tengah" : ["Palu"],
    "Sulawesi Tenggara" : ["Baubau", "Kendari"],
    "Sulawesi Utara" : ["Bitung", "Kotamobagu", "Manado" , "Tomohon"],
    "Sumatera Barat" : ["Bukittinggi", "Padang", "Padang Panjang", "Pariaman", "Payakumbuh", "Sawahlunto", "Solok"],
    "Sumatera Selatan" : ["Lubuklinggau", "Pagar Alam", "Palembang", "Prabumulih"],
    "Sumatera Utara" : ["Binjai", "Gunungsitoli", "Medan", "Padang Sidempuan", "Pematangsiantar", "Sibolga", "Tanjung Balai", "Tebing Tinggi"]
}

listProvinsi = list(daftarDaerah.keys())
listKota = ["Jakarta"]
kotaPilihan = "" # <- Variabel yang akan menyimpan kota yang dipilih
provPilihan = ""

### TKINTER untuk memilih kota
root = Tk()
root.title("Weather App - Pilih Kota")
root.resizable(0,0)

# Fungsi untuk menampilkan list kota berdasarkan pilihan provinsi
def pilihProvinsi(event):
    provinsi = combo1.get()
    listKota = daftarDaerah[provinsi]        
    combo2['values']=listKota
    combo2.set(listKota[0])

# Fungsi untuk mengambil string kota
def pilihKota():
    global kotaPilihan
    global provPilihan
    kotaPilihan = combo2.get() # Kota pilihan diambil dari value combobox2
    provPilihan = combo1.get() # Provinsi pilihan diambil dari value combobox1
    print(kotaPilihan)
    print(provPilihan)
    root.destroy()

# Menampilkan label Provinsi dan combobox list provinsi
label1 = Label(root, text="Provinsi", width=10, anchor="w")
label1.grid(row=0, column=0, padx=5, pady=5)
combo1 = ttk.Combobox(root, state="readonly", value=listProvinsi, width=40)
combo1.current(7)
combo1.bind("<<ComboboxSelected>>", pilihProvinsi)
combo1.grid(row=0, column=1, padx=5, pady=5)

# Menampilkan label Kota dan combobox list kota
label2 = Label(root, text="Kota", height=1, width=10, anchor="w")
label2.grid(row=1, column=0, padx=5, pady=5)
combo2 = ttk.Combobox(root, state="readonly", value=listKota, width=40)
combo2.grid(row=1, column=1, padx=5, pady=5)

# Menampilkan tombol Pilih kota
button = Button(root, text="Pilih kota", width=30, command=pilihKota)
button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()
### Akhir bagian TKINTER




### FLASK Untuk menampilkan data
app = Flask(__name__)

api_key = "3952cfa877429d1ad35c176b7a23a49d"

# Fungsi untuk mendapatkan latitude & longitude berdasarkan kota pilihan
def get_loc(kota):
    response = requests.get("https://api.openweathermap.org/geo/1.0/direct?q="+kotaPilihan+",ID&appid="+api_key)
    parse_json = json.loads(response.text) # File json hasil request
    lat = parse_json[0]['lat'] # Ambil latitude
    lon = parse_json[0]['lon'] # Ambil longitude
    if "local_names" in parse_json[0]:
        nama = parse_json[0]['local_names']['id'] # Ambil nama kota
    else:
        nama=kota
    return nama, lat, lon

# Fungsi untuk mendapatakn variabel-variabel cuaca berdasarkan lat & lon
def get_weather(lat, lon):
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&units=metric&lang=id&appid="+api_key)
        parse_json = json.loads(response.text)
        temp = parse_json['main']['temp']
        humid = parse_json['main']['humidity']
        press = parse_json['main']['pressure']
        windspd = parse_json['wind']['speed']
        if "rain" in parse_json:
            rain = parse_json['rain']['rain.1h']
        else:
            rain=0
        desc = parse_json['weather'][0]['description']
        return temp, humid, press, windspd, rain, desc
    except Exception as e:
        print("Error: "+str(e))
    

@app.route("/")
def main():
    # Memanggil fungsi get_loc untuk mendapatkan lat & lon berdasarkan kota pilihan
    dataKota = get_loc(kotaPilihan)

    # Memanggil fungsi get_weather untuk mendapatkan cuaca berdasarkan lat & lon
    dataCuaca = get_weather(str(dataKota[1]), str(dataKota[2]))

    return render_template('index.html', prov=provPilihan, kota=kotaPilihan, cuaca=dataCuaca)


# Bagian ini berfungsi agar web browser bisa dengan otomatis membuka webpage
import webbrowser
from threading import Timer;
def open_browser():
    webbrowser.open_new_tab('http://127.0.0.1:5000/')


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run()