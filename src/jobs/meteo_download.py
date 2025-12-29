import requests
import pandas as pd

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 40,
    "longitude": -4,
    "daily": "temperature_2m_max,precipitation_sum",
    "timezone": "Europe/Madrid"
}

response = requests.get(url, params=params, timeout=10)
data = response.json()

df = pd.DataFrame({
    "date": data["daily"]["time"],
    "temperature_2m_max": data["daily"]["temperature_2m_max"],
    "precipitation_sum": data["daily"]["precipitation_sum"],
})

print(df.head())
