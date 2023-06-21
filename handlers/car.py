import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

import config
from keyboards import keyboard_age_car, keyboard_type_engine


pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))


# Класс для хранения состояний
class Car(StatesGroup):
    car_age = State()
    car_type = State()
    car_engine_capacity = State()
    car_price = State()


def is_number(str: str):
    """Проверка числа.

    Функция проверяет, является ли строка вещественным числом.

    Args:
        str (str): Строка, которую необходимо проверить.

    Returns:
        bool: True, если строку можно преобразовать в вещественное число, иначе False.
    """
    try:
        float(str)
        return True
    except ValueError:
        return False


def separate_thousands(number):
    # Преобразование числа в строку
    number_str = str(number)

    # Разделение числа на триады
    separated = []
    for i in range(len(number_str)-1, -1, -3):
        separated.append(number_str[max(0, i-2):i+1])

    # Объединение триад с пробелами
    separated_str = ' '.join(reversed(separated))

    return separated_str


def get_exchange_rate():
    """Загрузка курса валюты.

    Функция, которая получает курс валюты с московской биржи.
    """
    url = "https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off"

    try:
        response = requests.get(url)
        data = response.json()
        usd = data["wap_rates"]["data"][0][4]
        eur = data["wap_rates"]["data"][1][4]
        return usd, eur
    except requests.exceptions.RequestException as e:
        print("Произошла ошибка при выполнении запроса:", e)
        return None


def recycling_collection(age: str) -> int:
    """Утилизационный сбор.

    Функция, которая считает утилизационный сбор.
    Args:
        age (str): возраст машины

    Returns:
        int: цена утилизационного сбора
    """
    if age == config.all_car_age[0]:
        return 3400
    else:
        return 5200


def duty_calculation(age: str, price: int, price_eur: int, engine_value: int, eur_rate: float) -> int:
    """Подсчет таможенной пошлины.

    Функция, которая считает таможенную пошлину в зависимости от возраста машины, 
    ее цены, объема двигателя.
    Args:
        age (str): возраст машины 
        price (int): цена машины
        price_eur (int): цена машины в евро
        engine_value (int): объем двигателя
        eur_rate (float): курс евро

    Returns:
        int: итоговая пошлина
    """
    duty = 0
    if age == config.all_car_age[0]:
        if price_eur <= 8500:
            duty = (price * 54) / 100
            duty_eur = duty / eur_rate
            if duty_eur < engine_value * 2.5:
                duty = engine_value * 2.5 * eur_rate
        elif 8501 <= price_eur <= 16700:
            duty = (price * 48) / 100
            duty_eur = duty / eur_rate
            if duty_eur < engine_value * 3.5:
                duty = engine_value * 3.5 * eur_rate
        elif 16701 <= price_eur < 42300:
            duty = (price * 48) / 100
            duty_eur = duty / eur_rate
            if duty_eur < engine_value * 5.5:
                duty = engine_value * 5.5 * eur_rate
        elif 42301 <= price_eur < 84500:
            duty = (price * 48) / 100
            duty_eur = duty / eur_rate
            if duty_eur < engine_value * 7.5:
                duty = engine_value * 7.5 * eur_rate
        elif 84501 <= price_eur < 169000:
            duty = (price * 48) / 100
            duty_eur = duty / eur_rate
            if duty_eur < engine_value * 15:
                duty = engine_value * 15 * eur_rate
        elif price_eur >= 169001:
            duty = (price * 48) / 100
            duty_eur = duty / eur_rate
            if duty_eur < engine_value * 20:
                duty = engine_value * 20 * eur_rate
    elif age == config.all_car_age[1]:
        if engine_value < 1000:
            duty = engine_value * 1.5 * eur_rate
        elif 1001 <= engine_value <= 1500:
            duty = engine_value * 1.7 * eur_rate
        elif 1501 <= engine_value <= 1800:
            duty = engine_value * 2.5 * eur_rate
        elif 1801 <= engine_value <= 2300:
            duty = engine_value * 2.7 * eur_rate
        elif 2301 <= engine_value <= 3000:
            duty = engine_value * 3 * eur_rate
        elif engine_value >= 3001:
            duty = engine_value * 3.6 * eur_rate
    elif age == config.all_car_age[2] or age == config.all_car_age[3]:
        if engine_value < 1000:
            duty = engine_value * 3 * eur_rate
        elif 1001 <= engine_value <= 1500:
            duty = engine_value * 3.2 * eur_rate
        elif 1501 <= engine_value <= 1800:
            duty = engine_value * 3.5 * eur_rate
        elif 1801 <= engine_value <= 2300:
            duty = engine_value * 4.8 * eur_rate
        elif 2301 <= engine_value <= 3000:
            duty = engine_value * 5 * eur_rate
        elif engine_value >= 3001:
            duty = engine_value * 5.7 * eur_rate
    return int(round(duty, 0))


def text_message(car_age: str, car_type: str, car_price: int, duty: int, price_rub: int,
                 recycling: int, car_engine_capacity: int | None = None, 
                 excise: int | None = None, vat: int | None = None) -> str:
    """Итоговый текст со всеми расчетами.

    Args:
        car_age (str): возраст автомобиля
        car_type (str): тип двигателя
        car_price (int): стоимость автомобиля
        duty (int): пошлина
        price_rub (int): цена в рублях
        recycling (int): утилизационный сбор
        car_engine_capacity (int | None, optional): Объем двигателя. Для электрокаров - None.
        excise (int | None, optional): акциза. Не для электрокаров - None.
        vat (int | None, optional): НДС. Не для электрокаров - None.

    Returns:
        str: текст расчета
    """
    # Импорт из конфига всех значений
    # Итого по Корее
    korea_uslugi = int(round(config.korea_uslugi * config.curr_usd, 0))
    korea_stoyanka = int(round(config.korea_stoyanka * config.curr_usd, 0))
    korea_peregon = int(round(config.korea_peregon * config.curr_usd))
    korea_parom = int(round(config.korea_parom * config.curr_usd))
    korea_summa = korea_uslugi + korea_stoyanka + korea_peregon + korea_parom
    # Стоимость ввоза
    tamozh_sbor = config.tamozh_sbor
    uslugi_brokera = config.uslugi_brokera
    car_sklad = config.car_sklad
    laboratoriya = config.laboratoriya
    peregon_company = config.peregon_company
    win_code = config.win_code
    spravka_gostinitsa = config.spravka_gostinitsa
    peregon_rastamozhka = config.peregon_rastamozhka

    import_cost = duty + tamozh_sbor + uslugi_brokera + car_sklad + laboratoriya +\
                peregon_company + win_code + spravka_gostinitsa +\
                peregon_rastamozhka + recycling

    text = f'''
*Ваш автомобиль*\:
Возраст \- {car_age}\.
Тип двигателя \- {car_type}\.'''
    # Объем двигателя есть у всех, кроме электрокаров
    if car_type != config.all_car_type[3]:
        text += f'\nОбъем двигателя \- {separate_thousands(car_engine_capacity)} см3\.'
    text += f'''
Цена \- {separate_thousands(car_price)} корейских вон\(KRW\)\.

*Итого по Корее*:
Услуги \- {separate_thousands(korea_uslugi)} RUB
Стоянка \- {separate_thousands(korea_stoyanka)} RUB
Перегон авто \- {separate_thousands(korea_peregon)} RUB
Паром \/ стивидорные работы \- {separate_thousands(korea_parom)} RUB
*Результат* \- {separate_thousands(korea_summa)} RUB

*Стоимость ввоза*:
Таможенная пошлина \- {separate_thousands(duty)} RUB'''
    # Акциза и НДС есть только у электрокаров
    if car_type == config.all_car_type[3]:
        text += f'''
Акциз \- {separate_thousands(excise)} RUB
НДС \- {separate_thousands(vat)} RUB'''
        import_cost += excise + vat
    text += f'''
Утилизационный сбор \- {separate_thousands(recycling)} RUB
Таможенный Сбор \- {separate_thousands(tamozh_sbor)} RUB
Услуга брокера \- {separate_thousands(uslugi_brokera)} RUB
Выгрузка/склад \- {separate_thousands(car_sklad)} RUB
Лаборатория \- {separate_thousands(laboratoriya)} RUB
Перегон авто до транспортной компании \- {separate_thousands(peregon_company)} RUB
Экспертиза ВИН кода \- {separate_thousands(win_code)} RUB
Справка с гостиницы \- {separate_thousands(spravka_gostinitsa)} RUB
Перегон авто во время растоможки \- {separate_thousands(peregon_rastamozhka)} RUB
*Итого* \- {separate_thousands(import_cost)} RUB

*Конечная стоимость* \- {separate_thousands(korea_summa + import_cost + price_rub)} RUB
'''
    return text


async def set_car_age(message: types.Message, state: FSMContext):
    """Начало расчета.

    Функция, которая запрашивает возраст автомобиля.
    """
    # Установка состояния ожидания ввода возраста автомобиля
    await state.set_state(Car.car_age.state)
    await message.answer('Выберете возраст машины:', reply_markup=keyboard_age_car)


async def set_car_type(message: types.Message, state: FSMContext):
    """Выбор типа двигателя автомобиля.

    Функция, которая запрашивает тип двигателя.
    """
    # Преобразовываем сообщение (возраст автомобиля) в нижний регистр
    car_age = message.text.lower()
    # Проверка, выбрал ли пользователь возраст из меню
    if car_age not in config.all_car_age:
        await message.answer('Некорректный ввод данных. Выберите возраст машины из списка: ' + ', '.join(config.all_car_age), reply_markup=keyboard_age_car)
        return
    # Сохранение возраста автомобиля в хранилище данных FSM
    await state.update_data(car_age=car_age)
    # Установка состояния ожидания ввода типа двигателя
    await state.set_state(Car.car_type.state)
    await message.answer('Выберете тип двигателя:', reply_markup=keyboard_type_engine)


async def set_car_engine_capacity(message: types.Message, state: FSMContext):
    """Выбор объема двигателя.

    Функция, которая запрашивает объем двигателя автомобиля.
    """
    # Преобразовываем сообщение (тип двигателя) в нижний регистр
    car_type = message.text.lower()
    # Проверка, выбрал ли пользователь тип двигателя из меню
    if car_type not in config.all_car_type:
        await message.answer('Некорректный ввод данных. Выберите тип двигателя из списка: ' + ', '.join(config.all_car_type), reply_markup=keyboard_type_engine)
        return
    # Сохранение типа двигателя в хранилище данных FSM
    await state.update_data(car_type=car_type)
    if car_type != 'электрический':
        # Установка состояния ожидания ввода объема двигателя автомобиля
        await state.set_state(Car.car_engine_capacity.state)
        await message.answer('Выберете объем двигателя в см3 (1 л = 1000 см3):', reply_markup=types.ReplyKeyboardRemove())
    else:
        # Установка состояния ожидания ввода стоимости автомобиля (для электрокаров)
        await state.set_state(Car.car_price.state)
        await message.answer('Введите стоимость автомобиля в корейских вонах(KRW):', reply_markup=types.ReplyKeyboardRemove())


async def set_car_price(message: types.Message, state: FSMContext):
    """Ввод стоимости автомобиля.

    Функция, которая запрашивает стоимость автомобиля.
    """
    car_engine_capacity = message.text
    # Проверка, ввел ли пользователь число
    if not is_number(car_engine_capacity):
        # Если пользователь ввел не число или число с ошибкой, то ему придет сообщение, чтобы он ввел корректное значение
        await message.answer('Ошибка. Пожалуйста, введите целое или вещественное число (например, 1600 или 250.78):')
        return
    # Сохранение объема двигателя в хранилище данных FSM
    await state.update_data(car_engine_capacity=car_engine_capacity)
    # Установка состояния ожидания ввода стоимости автомобиля 
    await state.set_state(Car.car_price.state)
    await message.answer('Введите стоимость автомобиля в корейских вонах(KRW):', reply_markup=types.ReplyKeyboardRemove())


async def cost_calculation(message: types.Message, state: FSMContext):
    """Расчет стоимости авто со всеми расходами.

    Функция, которая использует все раннее введенные данные и выдает результат сообщением.
    """
    car_price = message.text
    # Проверка, ввел ли пользователь число
    if not is_number(car_price):
        # Если пользователь ввел не число или число с ошибкой, то ему придет сообщение, чтобы он ввел корректное значение
        await message.answer('Ошибка. Пожалуйста, введите целое или вещественное число (например, 1600 или 250.78):')
        return
    # Сохранение стоимости автомобиля в хранилище данных FSM
    await state.update_data(car_price=car_price)
    # Получение всех раннее введенных данных
    car_data = await state.get_data()
    # Присвоение всех значений данных переменным
    car_age = car_data['car_age']
    car_type = car_data['car_type']
    # Стоимость автомобиля в вонах, рублях и евро
    car_price = int(car_data['car_price'])
    try:
        usd_rate, eur_rate = get_exchange_rate()
    except:
        usd_rate = config.curr_usd
        eur_rate = config.curr_eur
    price_rub = int(car_price * config.curr_krw)
    # price_usd = price_rub // usd_rate
    price_eur = price_rub // eur_rate

    # Стоимость утилизационного сбора
    util_rez = recycling_collection(car_age)

    # Если это не электрокар, то идет расчет пошлины и подготавливается сообщение на вывод
    if car_type != config.all_car_type[3]:
        car_engine_capacity = int(car_data['car_engine_capacity'])
        duty = duty_calculation(car_age, price_rub, price_eur, car_engine_capacity, eur_rate)
        text = text_message(car_age, car_type, car_price, duty, price_rub, util_rez, car_engine_capacity)
    else:
        power = 0
        # Пошлина электро
        duty = int(price_rub * 0.15)

        # Акциз электро (при 0 эти условия тут не нужны)
        if power <= 90:
            akciz = 0
        elif power >= 91 and power <= 150:
            akciz = power * 53
        elif power >= 151:
            akciz = power * 511

        # НДС электро
        nds = int((duty + util_rez + akciz) * 0.2)
        text = text_message(car_age, car_type, car_price, duty, price_rub, util_rez, excise=akciz, vat=nds)

    # Вывод сообщения после успешного выполнения функции
    await message.answer(text, parse_mode='MarkdownV2')

    # Подготовка PDF файла с отчетом и сохранение его на локальном диске
    c = canvas.Canvas(f"{message.from_user.id}.pdf", pagesize=A4)
    c.setFont("Arial", 13)
    text = text.replace('\\', '')
    text = text.replace('*', '')
    text_lines = text.split('\n')
    lines = 780
    for text in text_lines:
        c.drawString(80, lines, text)
        lines -= 23
    c.save()

    # Сообщение о готовности PDF файла
    await message.answer('Сформирован расчет PDF.\n Для скачивания выполните /save_pdf')

    # Закрытие хранилища данных FSM
    await state.finish()

async def save_pdf(message: types.Message):
    """Отправка PDF файла с отчетом.

    Функция, которая присылает в личные сообщения PDF файл с отчетом
    """
    try:
        # Путь к файлу PDF
        pdf_file_path = f'{message.from_user.id}.pdf'

        # Отправка файла PDF
        with open(pdf_file_path, 'rb') as pdf_file:
            await message.answer_document(pdf_file, caption='Готовый расчет в PDF')
    except:
        await message.answer('PDF еще не готов, сначала выполните команду /car')


def register_car_handlers(dp: Dispatcher):
    """Регистрация обработчиков событий.

    Регистрирует все обработчики событий, связанные с конвертацией валюты.
    """
    dp.register_message_handler(set_car_age, commands=['car'], state='*')
    dp.register_message_handler(set_car_type, state=Car.car_age)
    dp.register_message_handler(set_car_engine_capacity, state=Car.car_type)
    dp.register_message_handler(set_car_price, state=Car.car_engine_capacity)
    dp.register_message_handler(save_pdf, commands=['save_pdf'], state='*')
    dp.register_message_handler(cost_calculation, state=Car.car_price)
