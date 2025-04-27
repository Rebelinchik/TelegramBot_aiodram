import logging

logging.basicConfig(
    level=logging.INFO,
    filename="telegrambot_aiogram",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)
