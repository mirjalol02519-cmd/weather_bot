from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def generate_cities_keyboard(cities: list) -> ReplyKeyboardMarkup:
    # cities -> ["Toshkent", "Fargona"]

    keyboard = ReplyKeyboardBuilder()

    for city in cities:
        keyboard.button(text=city)

    keyboard.adjust(2)

    return keyboard.as_markup()
