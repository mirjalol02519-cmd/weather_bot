import asyncio
import logging

from pymysql import IntegrityError
from environs import Env
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import register_user, register_city, get_user_cities, clear_user_cities
from weather import get_weather_data
from keyboards import generate_cities_keyboard


env = Env()
env.read_env()

bot = Bot(token=env.str("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    telegram_id = message.from_user.id
    fullname = message.from_user.full_name

    try:
        register_user(telegram_id=telegram_id, fullname=fullname)
        await message.answer(text="Assalomu alaykum, muvaffaqiyatli ro'yxatga olindingiz !")
    except IntegrityError:
        await message.answer(text="Qaytganingizdan xursandmiz !")


@dp.message(Command(commands=["clear_cities"]))
async def clear_cities(message: Message):
    telegram_id = message.from_user.id

    clear_user_cities(telegram_id=telegram_id)

    await message.answer(
        text="Shaharlar ro'yxati tozalandi",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message()
async def answer_weather_data(message: Message):
    city_name = message.text
    weather_data, icon_code = get_weather_data(city_name=city_name)

    if weather_data:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Shaharni saqlash", callback_data=f"save:{city_name}")

        await message.answer_photo(
            photo=f"https://openweathermap.org/payload/api/media/file/{icon_code}.png",
            caption=weather_data,
            parse_mode="HTML",
            reply_markup=keyboard.as_markup()
        )
    else:
        await message.answer(text=f"{city_name} nomli shahar topilmadi")


@dp.callback_query(lambda call: "save" in call.data)
async def save_city(call: CallbackQuery):
    data = call.data                   
    city_name = data.split(":")[-1]     

    register_city(
        telegram_id=call.from_user.id,
        city_name=city_name
    )

    keyboard = InlineKeyboardBuilder()

    cities = get_user_cities(telegram_id=call.from_user.id)

    await call.message.answer(text="Shahar saqlandi", reply_markup=generate_cities_keyboard(cities=cities))

    keyboard.button(text="Shahar saqlandi ✅", callback_data="...")

    await call.message.edit_reply_markup(
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(lambda call: "..." in call.data)
async def show_alert(call: CallbackQuery):
    await call.answer(text="Shahar saqlangan", show_alert=True)


async def notify_admins():
    admins = env.list("ADMINS")

    for admin in admins:
        try:
            await bot.send_message(chat_id=admin, text="🤖 Bot (qayta) ishga tushdi!")
        except:
            pass


async def main():
    logging.basicConfig(level=logging.INFO)
    await notify_admins()
    await dp.start_polling(bot)

asyncio.run(main())
