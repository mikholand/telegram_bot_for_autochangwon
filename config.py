import os

from dotenv import load_dotenv

# Загрузка переменных и присвоение API-токена
load_dotenv('.env')
bot_token = os.getenv('BOT_API_TOKEN')
bot_username = os.getenv('BOT_USERNAME')

# Зарезервированный курс валют
curr_krw = 0.06
curr_usd = 80
curr_eur = 90

# Итого по Корее
korea_uslugi = 100
korea_stoyanka = 100
korea_peregon = 100
korea_parom = 100

# Стоимость ввоза
tamozh_sbor = 100
uslugi_brokera = 100
car_sklad = 100
laboratoriya = 100
peregon_company = 100
win_code = 100
spravka_gostinitsa = 100
peregon_rastamozhka = 100


all_car_age = ['до 3 лет', 'от 3 до 5 лет', 'от 5 до 7 лет', 'более 7 лет']
all_car_type = ['бензиновый', 'дизельный', 'гибридный', 'электрический']
