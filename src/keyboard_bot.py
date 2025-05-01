from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация")],
        [KeyboardButton(text="Добавить желание")],
        [KeyboardButton(text="Список желаний")],
        [KeyboardButton(text="Удалить желание")]
    ],
    resize_keyboard=True
)
