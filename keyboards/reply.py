from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Клавиатура для выбора возраста машины
keyboard_age_car = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='до 3 лет'),
            KeyboardButton(text='от 3 до 5 лет'),
            KeyboardButton(text='от 5 до 7 лет'),
            KeyboardButton(text='более 7 лет'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите возраст автомобиля',
)

# Клавиатура для выбора типа двигателя
keyboard_type_engine = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Бензиновый'),
            KeyboardButton(text='Дизельный'),
            KeyboardButton(text='Гибридный'),
            KeyboardButton(text='Электрический'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите тип двигателя',
)
