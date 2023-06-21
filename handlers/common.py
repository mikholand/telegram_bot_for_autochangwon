from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


async def start(message: types.Message, state: FSMContext):
    """Стартовая функция.

    Закрывает все состояния, если они были, и отправляет приветственное сообщение.
    """
    await state.finish()
    name = message.from_user.full_name
    text = '''
Здравствуйте, {0}! Я калькулятор бот autochangwon.
Могу расчитать стоимость авто до Владивостока в месте с таможней до получения ЕПТ и СБКТС.

Введи команду /car и следуй дальнейшим инструкциям.
Для отмены - введи /cancel или просто слово "отмена"
'''
    await message.answer(text.format(name))


async def cancel(message: types.Message, state: FSMContext):
    """Функция отмены.

    Закрывает все состояния, если они были и отправляет подтверждение прекращения действий.
    """
    await state.finish()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())


def register_common_handlers(dp: Dispatcher):
    """Регистрация обработчиков событий.

    Регистрирует все общие обработчики событий.
    """
    dp.register_message_handler(start, commands=['start', 'help'], state='*')
    dp.register_message_handler(cancel, commands=['cancel'], state='*')
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
