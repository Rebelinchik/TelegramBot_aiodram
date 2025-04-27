import logging

###создание логера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

###Обработчик для файла
file_handler = logging.FileHandler(filename="bot.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

###обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

###формат сообщений и присвавание формата файлу и консоли
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

###добавляем обработчики в логер
logger.addHandler(file_handler)
logger.addHandler(console_handler)
