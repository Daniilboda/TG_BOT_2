from pprint import pprint
import requests
from datetime import datetime, timedelta
import telebot
import sqlite3
import logging
from dotenv import load_dotenv
import os
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    filename="weather_bot.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

db = sqlite3.connect("weather_bot.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY
)
""")
db.commit()


def add_user(user_id: int):
    """Добавляет пользователя, если его нет."""
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    db.commit()


def count_users() -> int:
    """Возвращает количество пользователей."""
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]

def clear_users():
    """Удаляет все записи из таблицы users, оставляя таблицу пустой."""
    cursor.execute("DELETE FROM users")
    db.commit()



def telegram_bot(TOKEN_WEATHER_BOT):
    bot = telebot.TeleBot(TOKEN_WEATHER_BOT)
    @bot.message_handler(commands=['start'])
    def hello(message):
        add_user(message.chat.id)
        bot.send_message(message.chat.id,"Привет! Напиши название города в котором ты хочешь узнать погоду!")
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id,"По всем вопросам: @daniilboda")

    @bot.message_handler(commands=['info'])
    def info(message):
        bot.send_message(message.chat.id, "Новые боты скоро будут...")
    @bot.message_handler(commands=['clean_my_table'])
    def clean_my_table(message):
        if str(message.chat.id) == os.getenv('MY_ID'):
            clear_users()
            res = count_users()
            bot.send_message(message.chat.id, f'Результат очистки: {res}')
    @bot.message_handler(commands=['count_users'])
    def count(message):
        if str(message.chat.id) == os.getenv('MY_ID'):
            res = count_users()
            bot.send_message(message.chat.id, f'Запускали: {res}')
    @bot.message_handler(content_types=['text'])
    def send_txt(message):
        city = message.text.lower()
        my_dict_emoji = {
            'Clear': '\U00002600 Ясно',
            'Clouds': '\U00002601 Облачно',
            'Rain': '\U00002614 Дождь',
            'Drizzle': '\U00002614 Моросит',
            'Thunderstorm': '\U0001F329 Гроза',
            'Mist': '\U0001F32B Туман'
        }
        FLAGS = {
            "AD": "🇦🇩", "AE": "🇦🇪", "AF": "🇦🇫", "AG": "🇦🇬", "AI": "🇦🇮", "AL": "🇦🇱",
            "AM": "🇦🇲", "AO": "🇦🇴", "AQ": "🇦🇶", "AR": "🇦🇷", "AS": "🇦🇸", "AT": "🇦🇹",
            "AU": "🇦🇺", "AW": "🇦🇼", "AX": "🇦🇽", "AZ": "🇦🇿", "BA": "🇧🇦", "BB": "🇧🇧",
            "BD": "🇧🇩", "BE": "🇧🇪", "BF": "🇧🇫", "BG": "🇧🇬", "BH": "🇧🇭", "BI": "🇧🇮",
            "BJ": "🇧🇯", "BL": "🇧🇱", "BM": "🇧🇲", "BN": "🇧🇳", "BO": "🇧🇴", "BQ": "🇧🇶",
            "BR": "🇧🇷", "BS": "🇧🇸", "BT": "🇧🇹", "BV": "🇧🇻", "BW": "🇧🇼", "BY": "🇧🇾",
            "BZ": "🇧🇿", "CA": "🇨🇦", "CC": "🇨🇨", "CD": "🇨🇩", "CF": "🇨🇫", "CG": "🇨🇬",
            "CH": "🇨🇭", "CI": "🇨🇮", "CK": "🇨🇰", "CL": "🇨🇱", "CM": "🇨🇲", "CN": "🇨🇳",
            "CO": "🇨🇴", "CR": "🇨🇷", "CU": "🇨🇺", "CV": "🇨🇻", "CW": "🇨🇼", "CX": "🇨🇽",
            "CY": "🇨🇾", "CZ": "🇨🇿", "DE": "🇩🇪", "DJ": "🇩🇯", "DK": "🇩🇰", "DM": "🇩🇲",
            "DO": "🇩🇴", "DZ": "🇩🇿", "EC": "🇪🇨", "EE": "🇪🇪", "EG": "🇪🇬", "EH": "🇪🇭",
            "ER": "🇪🇷", "ES": "🇪🇸", "ET": "🇪🇹", "FI": "🇫🇮", "FJ": "🇫🇯", "FK": "🇫🇰",
            "FM": "🇫🇲", "FO": "🇫🇴", "FR": "🇫🇷", "GA": "🇬🇦", "GB": "🇬🇧", "GD": "🇬🇩",
            "GE": "🇬🇪", "GF": "🇬🇫", "GG": "🇬🇬", "GH": "🇬🇭", "GI": "🇬🇮", "GL": "🇬🇱",
            "GM": "🇬🇲", "GN": "🇬🇳", "GP": "🇬🇵", "GQ": "🇬🇶", "GR": "🇬🇷", "GS": "🇬🇸",
            "GT": "🇬🇹", "GU": "🇬🇺", "GW": "🇬🇼", "GY": "🇬🇾", "HK": "🇭🇰", "HM": "🇭🇲",
            "HN": "🇭🇳", "HR": "🇭🇷", "HT": "🇭🇹", "HU": "🇭🇺", "ID": "🇮🇩", "IE": "🇮🇪",
            "IL": "🇮🇱", "IM": "🇮🇲", "IN": "🇮🇳", "IO": "🇮🇴", "IQ": "🇮🇶", "IR": "🇮🇷",
            "IS": "🇮🇸", "IT": "🇮🇹", "JE": "🇯🇪", "JM": "🇯🇲", "JO": "🇯🇴", "JP": "🇯🇵",
            "KE": "🇰🇪", "KG": "🇰🇬", "KH": "🇰🇭", "KI": "🇰🇮", "KM": "🇰🇲", "KN": "🇰🇳",
            "KP": "🇰🇵", "KR": "🇰🇷", "KW": "🇰🇼", "KY": "🇰🇾", "KZ": "🇰🇿", "LA": "🇱🇦",
            "LB": "🇱🇧", "LC": "🇱🇨", "LI": "🇱🇮", "LK": "🇱🇰", "LR": "🇱🇷", "LS": "🇱🇸",
            "LT": "🇱🇹", "LU": "🇱🇺", "LV": "🇱🇻", "LY": "🇱🇾", "MA": "🇲🇦", "MC": "🇲🇨",
            "MD": "🇲🇩", "ME": "🇲🇪", "MF": "🇲🇫", "MG": "🇲🇬", "MH": "🇲🇭", "MK": "🇲🇰",
            "ML": "🇲🇱", "MM": "🇲🇲", "MN": "🇲🇳", "MO": "🇲🇴", "MP": "🇲🇵", "MQ": "🇲🇶",
            "MR": "🇲🇷", "MS": "🇲🇸", "MT": "🇲🇹", "MU": "🇲🇺", "MV": "🇲🇻", "MW": "🇲🇼",
            "MX": "🇲🇽", "MY": "🇲🇾", "MZ": "🇲🇿", "NA": "🇳🇦", "NC": "🇳🇨", "NE": "🇳🇪",
            "NF": "🇳🇫", "NG": "🇳🇬", "NI": "🇳🇮", "NL": "🇳🇱", "NO": "🇳🇴", "NP": "🇳🇵",
            "NR": "🇳🇷", "NU": "🇳🇺", "NZ": "🇳🇿", "OM": "🇴🇲", "PA": "🇵🇦", "PE": "🇵🇪",
            "PF": "🇵🇫", "PG": "🇵🇬", "PH": "🇵🇭", "PK": "🇵🇰", "PL": "🇵🇱", "PM": "🇵🇲",
            "PN": "🇵🇳", "PR": "🇵🇷", "PS": "🇵🇸", "PT": "🇵🇹", "PW": "🇵🇼", "PY": "🇵🇾",
            "QA": "🇶🇦", "RE": "🇷🇪", "RO": "🇷🇴", "RS": "🇷🇸", "RU": "🇷🇺", "RW": "🇷🇼",
            "SA": "🇸🇦", "SB": "🇸🇧", "SC": "🇸🇨", "SD": "🇸🇩", "SE": "🇸🇪", "SG": "🇸🇬",
            "SH": "🇸🇭", "SI": "🇸🇮", "SJ": "🇸🇯", "SK": "🇸🇰", "SL": "🇸🇱", "SM": "🇸🇲",
            "SN": "🇸🇳", "SO": "🇸🇴", "SR": "🇸🇷", "SS": "🇸🇸", "ST": "🇸🇹", "SV": "🇸🇻",
            "SX": "🇸🇽", "SY": "🇸🇾", "SZ": "🇸🇿", "TC": "🇹🇨", "TD": "🇹🇩", "TF": "🇹🇫",
            "TG": "🇹🇬", "TH": "🇹🇭", "TJ": "🇹🇯", "TK": "🇹🇰", "TL": "🇹🇱", "TM": "🇹🇲",
            "TN": "🇹🇳", "TO": "🇹🇴", "TR": "🇹🇷", "TT": "🇹🇹", "TV": "🇹🇻", "TW": "🇹🇼",
            "TZ": "🇹🇿", "UA": "🇺🇦", "UG": "🇺🇬", "UM": "🇺🇲", "US": "🇺🇸", "UY": "🇺🇾",
            "UZ": "🇺🇿", "VA": "🇻🇦", "VC": "🇻🇨", "VE": "🇻🇪", "VG": "🇻🇬", "VI": "🇻🇮",
            "VN": "🇻🇳", "VU": "🇻🇺", "WF": "🇼🇫", "WS": "🇼🇸", "YE": "🇾🇪", "YT": "🇾🇹",
            "ZA": "🇿🇦", "ZM": "🇿🇲", "ZW": "🇿🇼",
        }

        if message.text.lower().strip() == 'мяу':
            bot.send_message(message.chat.id, 'https://www.youtube.com/shorts/JJgr_R35zsE', disable_web_page_preview=False)

        elif message.text.lower().strip() == 'мур':
            bot.send_message(message.chat.id, 'https://www.youtube.com/shorts/dpkOQ3sWGtk', disable_web_page_preview=False)

        else:
            try:
                r = requests.get(f'https://api.openweathermap.org//data/2.5//weather?q={city}&appid={os.getenv('OPEN_WEATHER_TOKEN')}&units=metric')
                # print(f'https://api.openweathermap.org//data/2.5//weather?q={city}&appid={os.getenv('open_weather_token')}&units=metric')
                data = r.json()
                # pprint(data)

                date_now = (datetime.now() + timedelta(seconds=data['timezone'])).strftime('%d.%m.%Y %H:%M')
                country = data['sys']['country']
                city = data['name']
                cur_weather = data['main']['temp']
                feels_like = int(data['main']['feels_like'])
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                weather_desc = data['weather'][0]['main']
                if weather_desc in my_dict_emoji:
                    weather_desc = my_dict_emoji[weather_desc]
                if feels_like > 30:
                    feels_like = f'\U0001F975 Ощущается как: {int(feels_like)}°С'
                elif feels_like < -20:
                    feels_like = f'\U0001F976 Ощущается как: {int(feels_like)}°С'
                else:
                    feels_like = f'Ощущается как: {int(feels_like)}°С'
                bot.send_message(message.chat.id, f'Текущая дата и время: {date_now}\n{FLAGS[country]} Страна: {country}\nГород: {city}\n'
                      f'Погода сейчас: {int(cur_weather)}°С\n{weather_desc}\n\U0001F4A7 Влажность: {humidity} %\n\U0001F4A8 Скорость ветра: {wind_speed} м/c\n{feels_like}')
            except Exception as ex:
                bot.send_message(message.chat.id, "Напиши название города в котором ты хочешь узнать погоду!")
                logging.exception(ex)
                logging.info(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv("open_weather_token")}&units=metric')
                print(ex)


    bot.polling()

def main():
    telegram_bot(os.getenv('TOKEN_WEATHER_BOT'))

if __name__ == '__main__':
    main()