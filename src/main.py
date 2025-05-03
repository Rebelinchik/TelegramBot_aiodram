import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv

# свои модули
from logging_bot import logger
from memory_bot import FSMContext, MemoryBot
from keyboard_bot import keyboard
from sql import *
from scripts import create_link_in_text

###ТОКЕН
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.error("TOKEN не найден в файле")
    exit(1)


###КЛАСС БОТА
class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher()
        ###Клавиатура
        self.button = keyboard
        ###Регистрация всех хендлеров
        self.register_hundlers()

    def register_hundlers(self):
        self.dp.message.register(self.start, Command("start"))
        self.dp.message.register(self.registration_on_db, F.text == "Регистрация")
        self.dp.message.register(self.link, F.text == "Добавить желание")
        self.dp.message.register(self.get_link, MemoryBot.waiting_link)
        self.dp.message.register(self.show_list, F.text == "Список желаний")
        self.dp.message.register(self.delete_link, F.text == "Удалить желание")
        self.dp.message.register(self.get_num_link, MemoryBot.waiting_del_link)
        self.dp.message.register(
            self.add_user_pair, F.text == "Добавить вторую половинку"
        )
        self.dp.message.register(self.get_user_pair, MemoryBot.waiting_pair)
        self.dp.message.register(self.other_text)

    ###Хендлеры
    # Старт
    async def start(self, message: types.Message):
        id = message.from_user.id
        username = message.from_user.username
        logger.info(f"Пользователь {id} запустил бота через /start")
        await message.answer(
            f"Здравствуй {username}.\n Пожалуйста зарегистрируйся",
            reply_markup=self.button,
        )

    # регистрация в базе данных
    async def registration_on_db(self, message: types.Message):
        id = message.from_user.id
        username = message.from_user.username
        try:
            if not ischeck_user_in_db(int(id)):
                add_user_db(int(id), str(username))
                logger.info(f"Пользователь {id} зарегистрирован в базе данных")
                await message.answer(f"{username}, вы зарегистированны в базе данных")
            else:
                await message.answer(
                    "Вы уже зарегистрированы", reply_markup=self.button
                )
        except Exception as e:
            logger.error(f"Произошла ошибка при регистрации в главном файле: {e}")

    # Запуск добавления ссылки в строку пользователя в базе данных
    async def link(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        if ischeck_user_in_db(int(id)):
            logger.info(f"Пользователь {id} начал запись ссылки")
            await message.answer(
                "Хорошо, поделись со мной желанием с маркетплейса",
                reply_markup=self.button,
            )
            await state.set_state(MemoryBot.waiting_link)
        else:
            await message.answer("Для начала зарегистрируйся", reply_markup=self.button)

    # обработка добавления ссылки
    async def get_link(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        username = message.from_user.username
        text = message.text

        if "http" in text:
            link = create_link_in_text(text)
            try:
                add_link_db(int(id), str(link))
                logger.info(f"Пользователь {id} сохранил свое желание")
                await message.answer(
                    f"Твоё желание сохранено, {username}",
                    reply_markup=self.button,
                )
                await state.clear()
                if ischeck_pair_on_user(id):
                    await self.bot.send_message(
                        chat_id=user_id_in_username(pair_in_user_id(id)),
                        text="Твоя вторая половинка добавила новое желание",
                    )
            except Exception as e:
                logger.error(
                    f"ошибка при сохранении ссылки пользователя {id} в основном коде: {e}"
                )
                await message.answer(
                    "Что то пошло не так, попробуйте позже", reply_markup=self.button
                )
        else:
            logger.error(
                f"В сообщении пользователя {id} нет ссылки, ссылка не сохранена"
            )
            await message.reply(
                "В этом сообщении нет ссылки на желание, твоё желание не сохранено",
                reply_markup=self.button,
            )
            await state.clear()

    # вывод списка желаний пользователя
    async def show_list(self, message: types.Message):
        id = message.from_user.id
        try:
            if not ischeck_user_in_db(id):
                logger.info(
                    f"Пользователя {id} нет в базе данных или его список желаний пуст"
                )
                await message.answer(
                    "Скорей всего тебя нет в базе данных или ты ничего не добавил в список желаний",
                    reply_markup=self.button,
                )
            else:
                logger.info(f"Пользователь {id} запросил список желаний:")
                await message.answer(
                    "Вот твой список желаний:", reply_markup=self.button
                )
                count = 1
                for link in upload_links(int(id)):
                    num_link = str(count) + ") " + link
                    await message.answer(num_link)
                    count += 1
                logger.info(
                    f"Пользователь {id} запросил список желаний: список желаний выдан пользовтелю"
                )
        except Exception as e:
            logger.error(
                f"У пользователя {id} при выгрузке ссылок в main произошла ошибка: {e}"
            )

    # запуск удаления ссылки(запрос номеров ссылок)
    async def delete_link(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        if ischeck_user_in_db(int(id)):
            logger.info(f"Пользователь {id} начал удаление ссылок:")
            await message.answer(
                "Напиши через пробел в порядке возрастания, какие желания нужно удалить",
            )
            await state.set_state(MemoryBot.waiting_del_link)
        else:
            logger.error(f"Действие незарегистрированного пользователя {id}")
            await message.answer("Для начала зарегистрируйся", reply_markup=self.button)

    # ожидание номеров ссылок
    async def get_num_link(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        text = message.text.split()
        if any(map(lambda n: type(n) != int, text)):
            try:
                del_link(int(id), text)
                await message.answer(
                    "Выбранные желания удалены, вот что осталось:",
                    reply_markup=self.button,
                )
                count = 1
                for link in upload_links(int(id)):
                    num_link = str(count) + ") " + link
                    await message.answer(num_link)
                    count += 1
                logger.info(f"Желания пользователя {id} удалены")
                await state.clear()
                if ischeck_pair_on_user(id):
                    await self.bot.send_message(
                        chat_id=user_id_in_username(pair_in_user_id(id)),
                        text="Твоя вторая половинка удалила некоторые свои желания",
                    )
            except Exception as e:
                logger.error(
                    f"У пользователя {id} произошла ошибка при удалении ссылок"
                )
                await message.answer(
                    "Произошла ошибка, попробуй позже", reply_markup=self.button
                )
                await state.clear()
        else:
            logger.info(f"Неудачная попытка удаления ссылок пользователя {id}")
            await message.answer(
                "В сообщении не только цифры, удаление не выполнено",
                reply_markup=self.button,
            )
            await state.clear()

    # запуск добавления пары пользователя
    async def add_user_pair(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        if ischeck_user_in_db(int(id)):
            logger.info(f"Пользователь {id} начал добавление своей пары")
            await message.answer(
                "Отправь мне @никнейм совей творой половинки, она должна быть зарегистрирована в моей базе данных. Ты так же автоматически устанавливаешься парой у твоей половинки",
            )
            await state.set_state(MemoryBot.waiting_pair)
        else:
            logger.error(f"Действие незарегистрированного пользователя {id}")
            await message.answer("Для начала зарегистрируйся", reply_markup=self.button)

    # ожидание добавления имя пользователя
    async def get_user_pair(self, message: types.Message, state: FSMContext):
        text = message.text
        id = message.from_user.id
        username = message.from_user.username
        if "@" in text:
            name = text[1:]
            if ischeck_username_in_db(name):
                add_pair(id, name)
                await self.bot.send_message(
                    chat_id=user_id_in_username(name),
                    text=f"Пользователь {username} синхронизировал ваши желания)",
                )
                await message.answer(
                    f"Твоя вторая половинка {name} успешно привязана к твоему аккаунту"
                )
                await state.clear()
                logger.info(
                    f"Пользователь {id} завершил добавление пользователя успешно"
                )
            else:
                await message.answer(
                    f"Пользователя {name} нет в базе данных, попроси его что бы он зарегистрировался"
                )
                await state.clear()
                logger.info(
                    f"Пользователь {id} отправил несуществующего пользователя в БД. Добавление завершено"
                )
        else:
            await message.answer("Ты не отправил имя пользователя")
            await state.clear()
            logger.info(
                f"Пользователь {id} не отправил имя пользователя. Добавления перы завершено"
            )

    # Не обрабатываемые сообщения
    async def other_text(self, message: types.Message):
        id = message.from_user.id
        text = message.text
        logger.info(f"Пользователь {id} отправил необрабатываемое сообщение")
        await message.answer(
            f"Я обрабатываю только команды с вcтроенной клавиатуры",
            reply_markup=self.button,
        )
        if text:
            await message.answer(
                f"Твоё сообщение: {text}",
                reply_markup=self.button,
            )

    ###Запуск бота
    async def run(self):
        logger.info("Бот запущен")
        await self.dp.start_polling(self.bot)


###точка входа
if __name__ == "__main__":
    try:
        bot = TelegramBot()
        asyncio.run(bot.run())
    except Exception as e:
        logger.error(e)
