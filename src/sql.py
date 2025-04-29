import sqlite3
import os

from dotenv import load_dotenv
from logging_bot import logger
from aiogram import types

load_dotenv()
db_path = os.getenv("SQLITE3_LINK")
connect_db = sqlite3.connect(db_path)


###Проверка есть ли user в БД
def ischeck_user_in_db(user_id: int):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users_data WHERE user_id = ?", (user_id,))
            return cur.fetchone()[0] > 0
    except Exception as e:
        logger.error(f"Ошибка при проверке наличия пользователя в базе данных: {e}")


###Проверка есть ли пользователь и есть ли желания у пользователя
def ischeck_link_in_db(user_id: int):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute("SELECT links FROM users_data WHERE user_id = ?", (user_id,))
            value = cur.fetchone()
            if value and len(value[0]) != 0:
                return True
            else:
                return False
    except Exception as e:
        logger.error(f"Ошибка при проверке наличия пользователя в базе данных: {e}")


###Добавление user в БД
def add_user_db(user_id: int, username: str):
    links = ""
    pair = ""
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users_data (user_id, username, links, pair) VALUES (?, ?, ?, ?)",
                (user_id, username, links, pair),
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Произошла ошибка при регистрации в функии регистрации: {e}")


###Добавление ссылки
def add_link_db(user_id: int, link: str):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute("SELECT links FROM users_data WHERE user_id = ?", (user_id,))
            new_value = cur.fetchone()[0] + link
            cur.execute(
                "UPDATE users_data SET links = ? WHERE user_id = ?",
                (new_value, user_id),
            )
            conn.commit()
    except Exception as e:
        logger.info(f"При добавлении ссылки в sql произошла ошибка: {e}")


###Вывод списка желаний
def upload_links(message: types.Message, user_id: int):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute("SELECT links FROM users_data WHERE user_id = ?", (user_id,))
            return cur.fetchone()[0].split()
    except Exception as e:
        logger.error(f"При выгрузке ссылок в sql произошла ошибка: {e}")
