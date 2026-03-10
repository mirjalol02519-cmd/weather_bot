from requests import get as GET
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("WEATHER_TOKEN")


def get_weather_data(city_name: str) -> str | None:
    URL = "https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {
        "q": city_name,
        "appid": TOKEN,
        "lang": "ru",
        "units": "metric",
    }

    response = GET(url=URL, params=PARAMS)

    data = response.json() # JSON -> Python

    if data.get("cod") == "404":
        return None

    temp = data.get("main").get("temp")             # 9.25 C
    temp_min = data.get("main").get("temp_min")     # 7.25 C
    temp_max = data.get("main").get("temp_max")     # 10.25 C
    pressure = data.get("main").get("pressure")     # 1008 Pa
    humidity = data.get("main").get("humidity")     # 75 %
    icon_code = data.get("weather")[0].get("icon")
    weather_code = data.get("weather")[0].get("id")

    text = f"🌆 Bugun <b>{city_name.capitalize()}</b> dagi havo haqida"

    text += f"\n\n🌡️ Harorat: <b>{temp} °C</b>"
    text += f"\n🥶 Minimal harorat: <b>{temp_min} °C</b>"
    text += f"\n🥵 Maksimal harorat: <b>{temp_max} °C</b>"

    text += f"\n\n💧 Namlik: <b>{humidity} %</b>"
    text += f"\n⬇️ Bosim: <b>{pressure} Pa</b>"

    if temp <= 0:
        text += f"\n\nIssiqroq kiyinishingizni maslahat beraman 🧤 ..."
    elif temp > 10 and temp < 20:
        text += f"\nJudaaaa sayir qiladigan havo bo'lyaptidaaaa ..."
    elif temp > 35:
        text += f"\n\nUyda o'tirishni maslahat beraman, tashqari jazirama ..."

    if 200 <= weather_code < 300:
        text += "\n\nMomaqaldiroq kutilmoqda, zontik ovoling"
    elif 300 <= weather_code < 400:
        text += "\n\nPaqirdan quygandek yog'yapti, zontik esdan chiqmasin"
    elif 500 <= weather_code < 600:
        text += "\n\nZontik olishni maslahat beraman, yomg'ir kuchayishi ham mumkin"
    elif 600 <= weather_code < 700:
        text += "\n\nEtik kiyib chiq"
    elif 700 <= weather_code < 800:
        text += "\n\nNamlik juda kuchli, tuman ham bor"
    elif 800 <= weather_code < 900:
        text += "\n\nAjoyib oydin kun/tun bo'lyapti lekin boru"

    return text, icon_code

