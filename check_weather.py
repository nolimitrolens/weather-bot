import requests
from datetime import datetime

PUSHOVER_USER_KEY = "u8zazsfgi28saqs43i1bfsthgkrzam"
PUSHOVER_API_TOKEN = "aTKDuK2eKECqz0nGJi5hrQGypABt8M"
OPENWEATHER_API_KEY = "8f071432812b37b94e236ef9c63b31f1"
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
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=imperial"
    return requests.get(url).json()

def build_alert(d):
    alerts = []
    if d['temp']['min'] < 34:
        alerts.append("🧊 Frost claws at the roots.")
    if d['temp']['max'] > 95:
        alerts.append("🔥 The Grove withers in firelight.")
    if d.get('wind_gust', 0) > 25:
        alerts.append("💨 Wind howls. Secure all spirits.")
    if d.get('rain', 0) > 0.3:
        alerts.append("🌧️ The sky bleeds. Pause the flow.")
    if d.get('humidity', 100) < 30 and d['temp']['max'] > 85:
        alerts.append("🌬️ Air runs dry. Mist the moss. Aid the clover.")

    today = datetime.now()
    if f"{today.month}-{today.day}" in ["3-20", "6-21", "9-22", "12-21"]:
        alerts.append("🩸 The Hollow calls. Kneel beneath the branches and speak.")

    if not alerts and today.day % 3 == 0:
        vibes = [
            "🕯️ No danger today… but the trees remember.",
            "🌑 A silence hangs. The Hollow watches.",
            "🦴 Nothing stirs—but roots still dream.",
            "🍃 A calm day… for now.",
            "👁️ Something unseen stirs beneath the moss."
        ]
        alerts.append(vibes[today.day % len(vibes)])

    forecast = f"Low: {d['temp']['min']}°F\nHigh: {d['temp']['max']}°F\nHumidity: {d['humidity']}%\nWind: {d.get('wind_gust', 0)} mph\nRain: {d.get('rain', 0)} in"
    return "\n".join(alerts) + "\n\n🌡️ Forecast:\n" + forecast

def main():
    weather = get_weather()
    today = weather['daily'][0]
    msg = build_alert(today)
    if msg:
        send_pushover(msg)

if __name__ == "__main__":
    main()
