import asyncio
import logging
import sys

import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from private import TOKEN, PHOTO, URL

dp = Dispatcher()
bot = Bot(TOKEN)


@dp.message(Command("start"))
@dp.callback_query(F.data == "menu")
async def menu(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Запуск 🔥")],
        [
            types.KeyboardButton(text="Открыть окно 🔒"),
            types.KeyboardButton(text="Поговорить об Аишках")
        ],
        [types.KeyboardButton(text="Пробить лоха")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Вы слышали про VegaCoin?", reply_markup=keyboard)


@dp.message(Command("menu"))
@dp.message(F.text.lower() == "запуск 🔥")
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="VegaCoin🪙",
        web_app=WebAppInfo(url=URL["clickApp"])
    ))
    builder.row(types.InlineKeyboardButton(
        text="Info",
        web_app=WebAppInfo(url=URL["vega"])
    ))

    await message.answer('Выберите ссылку', reply_markup=builder.as_markup(), )





@dp.message(F.text.lower() == "поговорить об аишках")
async def with_puree(message: types.Message):
    await message.reply("Вызываем")


@dp.message(F.text.lower() == "открыть окно 🔒")
async def with_puree(message: types.Message):
    await message.reply("Скуфы этого не одобряют")


async def get_ip_address():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL["ipAPI"])
        data = response.json()
        return data['ip']


async def get_user_info(user_id):
    user = await bot.get_chat(user_id)
    return user


@dp.message(Command("me"))
@dp.message(F.text.lower() == "пробить лоха")
async def get_user_information(message: types.Message):
    try:
        user_info = await get_user_info(message.from_user.id)
        ip_address = await get_ip_address()

        if user_info:
            info_message = (
                    "╔══════════════════════╗\n" +
                    "║ Информация о вашем акаунте ║\n" +
                    "╟──────────────────────╢\n" +
                    f"👥 Тег: {user_info.username}\n"
                    f"👤 Имя: {user_info.first_name}\n"
                    f"🧔 Фамилия: {user_info.last_name}\n"
                    f"🆔 ID: {user_info.id}\n"
            )
            if ip_address:
                info_message += f"🌐 IP: {ip_address}\n"

            await message.answer(info_message)
        else:
            await message.answer("Не удалось получить информацию о вашем аккаунте.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


# Ответ на присланные файлы (перечисление файлов в списке хейждера)
@dp.message(F.content_type.in_({'photo', 'sticker'}))
async def handle_all_files(message: types.Message):
    image_from_url = URLInputFile(PHOTO["pepa"])
    await message.answer_photo(
        photo=image_from_url,
        caption="Ну и нахуй ты это скинул, еблан?"
    )


async def main() -> None:
    # bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
