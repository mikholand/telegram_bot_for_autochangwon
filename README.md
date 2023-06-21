# telegram_bot_for_autochangwon
Telegram bot Autochangwon Calculator. <br><br>
Это Telegram-бот, разработанный для помощи пользователям в расчете стоимости
доставки автомобилей из Кореи с использованием сайта Autochangwon. Бот
работает в автономном режиме и может быть использован по ссылке 
[Autochangwon_calculator_bot](https://t.me/Autochangwon_calculator_bot).

## Особенности
- Расчет стоимости доставки автомобилей из Кореи.
- Подробная разбивка расходов, включая таможенные пошлины, налоги и плату
за транспортировку.
- Интеграция с MOEX (московской биржей) для получения актуальных курсов валют.
- Интерфейс с кнопками для удобного взаимодействия.

## Запуск бота
Для использования этого скрипта вам нужно следовать следующей инструкции:
1. Установите Python 3.10 с [официального сайта](https://www.python.org/).
2. Клонируйте репозиторий или загрузите файлы кода:
```sh
git clone https://github.com/mikholand/telegram_bot_for_autochangwon.git
```
3. Установите необходимые зависимости с помощью pip:
```sh
pip install -r requirements.txt
```
4. Создайте нового бота и получите API-токен от BotFather в Telegram.
5. Измените файл .env.example в корневой папке проекта на .env и замените
токена из пункта 4.
6. Запустите скрипт:
```sh
python main.py
```

## Использование
После запуска бота вы можете взаимодействовать с ним через приложение 
Telegram. Начните чат с ботом и следуйте инструкциям, чтобы получить 
доступ к различным функциям:
1. /car - начало работы с калькулятором.
2. /save_pdf - получить PDF-файл с расчетом.
3. /cancel или "Отмена" - Отменить текущее действие.

## Лицензия
Этот скрипт распространяется на условиях лицензии MIT. 
Подробности смотрите в файле
[LICENSE](https://github.com/mikholand/telegram_bot_for_group/blob/master/LICENSE).

## Disclaimer
Это всего лишь пример кода, написанного мной. Расчеты могут отличаться
от действующего сайта и бота.

## Контакты
Михно Олег - [Telegram](https://t.me/mikholand) - mikholand@gmail.com

GitHub: [https://github.com/mikholand](https://github.com/mikholand)

LinkedIn: [https://www.linkedin.com/in/mikholand/](https://www.linkedin.com/in/mikholand/)
