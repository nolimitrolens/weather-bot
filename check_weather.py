import requests
from datetime import datetime

PUSHOVER_USER_KEY = "u8zazsfgi28saqs43i1bfsthgkrzam"
PUSHOVER_API_TOKEN = "ab9g4rom4m29syu7oidm6patsx8rp6"
OPENWEATHER_API_KEY = "6585880ac4cd8619d66a2237d2341623"
LAT = 38.8
LON = -89.9

def send_pushover(message):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": "🌲 Bonsai Weather Alert",
        "sound": "alien"
    })

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=imperial"
    res = requests.get(url)
    try:
        res.raise_for_status()
        return res.json()
    except Exception as e:
        send_pushover(f"💥 Weather API error: {e}")
        return None

def build_alert(data):
    alerts = []
    today = datetime.now().date()
    day_data = [d for d in data['list'] if datetime.fromtimestamp(d['dt']).date() == today]

    if not day_data:
        return "⚠️ No weather data found for today."

    temps = [d['main']['temp'] for d in day_data]
    min_temp = min(temps)
    max_temp = max(temps)
    humidity = sum([d['main']['humidity'] for d in day_data]) // len(day_data)
    wind = max([d['wind']['speed'] for d in day_data])
    rain = sum([d.get('rain', {}).get('3h', 0) for d in day_data])

    if min_temp < 34:
        alerts.append("🧊 Frost claws at the roots.")
    if max_temp > 95:
        alerts.append("🔥 The Grove withers in firelight.")
    if wind > 25:
        alerts.append("💨 Wind howls. Secure all spirits.")
    if rain > 0.3:
        alerts.append("🌧️ The sky bleeds. Pause the flow.")
    if humidity < 30 and max_temp > 85:
        alerts.append("🌬️ Air runs dry. Mist the moss. Aid the clover.")

    if not alerts and datetime.now().day % 3 == 0:
        alerts.append("🕯️ No danger today… but the trees remember.")

    forecast = f"Low: {min_temp}°F\\nHigh: {max_temp}°F\\nHumidity: {humidity}%\\nWind: {wind} mph\\nRain: {round(rain, 2)} in"
    return "\\n".join(alerts) + "\\n\\n🌡️ Forecast:\\n" + forecast

def main():
    data = get_weather()
    if data:
        msg = build_alert(data)
        if msg:
            send_pushover(msg)

if __name__ == "__main__":
    main()
