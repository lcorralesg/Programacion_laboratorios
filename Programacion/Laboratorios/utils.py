import requests
from datetime import datetime

def obtener_datos_clima():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Lima&appid=bf7affab900e00c1e1febb54775f9185"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Convertir la temperatura de Kelvin a Celsius
        temperatura_kelvin = data['main']['temp']
        temperatura_celsius = temperatura_kelvin - 273.15
        # Formatear la temperatura a dos decimales
        temperatura_formateada = "{:.2f}".format(temperatura_celsius)
        descripcion = data['weather'][0]['description']
        fecha_hora = data['dt']
        # Convertir la fecha y hora en un formato legible
        fecha_hora_actual = datetime.fromtimestamp(fecha_hora).strftime('%Y-%m-%d %H:%M:%S')
        return temperatura_formateada, descripcion, fecha_hora_actual
    else:
        return None, None, None