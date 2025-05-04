from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация"), KeyboardButton(text="Добавить желание")],
        [KeyboardButton(text="Список желаний"), KeyboardButton(text="Удалить желание")],
        [KeyboardButton(text="Добавить вторую половинку"), KeyboardButton(text="Желания половинки")],
    ],
    resize_keyboard=True,
)

stop_link = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Закончить добавление желаний")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

