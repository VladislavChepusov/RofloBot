import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, WebAppInfo, URLInputFile
from aiogram.utils.markdown import hide_link

from private import TOKEN

dp = Dispatcher()

@dp.message()
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Мир Вегагаза", web_app=WebAppInfo(url="https://itproger.com"))
    markup.add(button)
    await message.answer("ВегаКоин близко! Посетите Мир Вегагаза.", reply_markup=markup)


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
    image_from_url = URLInputFile("https://preview.redd.it/bd7q2jvcght21.jpg?auto=webp&s=f36a77a9f383441047a7e3b3f8fa88870d2f700f")
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
