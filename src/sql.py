import sqlite3
import os

from dotenv import load_dotenv
from logging_bot import logger

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


###Проверка пользователя по username для добавления пары
def ischeck_username_in_db(username: str):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM users_data WHERE username = ?", (username,)
            )
            return cur.fetchone()[0] > 0
    except Exception as e:
        logger.error(f"Ошибка при проверке наличия username в базе данных: {e}")


###Проверка наличия пары пользователя
def ischeck_pair_on_user(user_id: int) -> bool:
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute("SELECT pair FROM users_data WHERE user_id = ?", (user_id,))
            return len(cur.fetchone()[0]) > 0
    except Exception as e:
        logger.error(f"Ошибка при проверке наличия pair в базе данных: {e}")


###Доставание user_id по username
def user_id_in_username(username) -> int:
    with connect_db as conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users_data WHERE username = ?", (username,))
        return int(cur.fetchone()[0])


###Доставание username по user_id
def username_in_user_id(user_id: int) -> str:
    with connect_db as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users_data WHERE user_id = ?", (user_id,))
        return str(cur.fetchone()[0])


###Лоставание пары по user_id
def pair_in_user_id(user_id: int) -> str:
    with connect_db as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT pair FROM users_data WHERE user_id = ?",
            (user_id,)
        )
        return str(cur.fetchone()[0])


###Добавление user в БД
def add_user_db(user_id: int, username: str):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users_data (user_id, username, links, pair) VALUES (?, ?, ?, ?)",
                (user_id, username, "", ""),
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
def upload_links(user_id: int) -> list:
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute("SELECT links FROM users_data WHERE user_id = ?", (user_id,))
            return cur.fetchone()[0].split()
    except Exception as e:
        logger.error(
            f"У пользователя {user_id} при выгрузке ссылок в sql произошла ошибка: {e}"
        )


###удаление ссылок
def del_link(user_id: int, text: list):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute("SELECT links FROM users_data WHERE user_id = ?", (user_id,))
            links_list = cur.fetchone()[0].split()
            for i in sorted((int(x) for x in text), reverse=True):
                count = int(i) - 1
                del links_list[count]

            if len(links_list) != 0:
                links = "\n".join(links_list)
                cur.execute(
                    "UPDATE users_data SET links = ? WHERE user_id = ?",
                    (links, user_id),
                )
            else:
                cur.execute(
                    "UPDATE users_data SET links = ? WHERE user_id = ?",
                    ("", user_id),
                )
            conn.commit()
    except Exception as e:
        logger.error(
            f"У пользователя {user_id} при удалении ссылки произошла ошибка в sql: {e}"
        )


### добавление пары
def add_pair(user_id: int, pair: str):
    try:
        with connect_db as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users_data SET pair = ? WHERE user_id = ?", (pair, user_id)
            )
            cur.execute(
                "UPDATE users_data SET pair = ? WHERE user_id = ?",
                (username_in_user_id(user_id), user_id_in_username(pair)),
            )
            conn.commit()
    except Exception as e:
        logger.error(
            f"У пользователя {user_id} произошла ошибка при добавлении пары: {e}"
        )
