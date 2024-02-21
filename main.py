import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, URLInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hide_link

from private import TOKEN, PHOTO, URL


dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Открыть окно 🔒")],
        [types.KeyboardButton(text="Поговорить об Аишках")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Вы слышали про VegaCoin?", reply_markup=keyboard)


@dp.message(Command("inline_url"))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Наш сайт ",
        web_app=WebAppInfo( url=URL["vega"])
       )
    )
    await message.answer('Выберите ссылку', reply_markup=builder.as_markup(), )


@dp.message(F.text.lower() == "поговорить об аишках")
async def with_puree(message: types.Message):
    await message.reply("Вызываем")


@dp.message(F.text.lower() == "открыть окно 🔒")
async def with_puree(message: types.Message):
    await message.reply("Скуфы этого не одобряют")


# Ответ при вызове команды
@dp.message(Command("ss"))
async def cmd_hidden_link(message: Message):
    logging.debug('КОМАНДА СС')
    await message.answer(
        f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
        f"Документация Telegram: *существует*\n"
        f"Пользователи: *не читают документацию*\n"
        f"Груша:"
    )


# Ответ на присланные файлы (перечисление файлов в списке хейждера)
@dp.message(F.content_type.in_({'photo', 'sticker'}))
async def handle_all_files(message: types.Message):
    image_from_url = URLInputFile(PHOTO["pepa"])
    await message.answer_photo(
        photo=image_from_url,
        caption="Ну и нахуй ты это скинул, еблан?"
    )


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
