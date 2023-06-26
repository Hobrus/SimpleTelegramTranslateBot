import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = "TOKEN"
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

lanquages = {
    "ru": "Русский",
    "en": "English",
    "es": "Espanol",
}


class User:
    dest_lang = "ru"


def translate(text, src_lang, dest_lang):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": text,
        "target": dest_lang,
        "source": src_lang
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "TOKEN",
        "X-RapidAPI-Host": "TOKEN"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()["data"]["translations"][0]["translatedText"]


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for lang in lanquages.values():
        keyboard.add(lang)
    await message.answer("Привет! Выбери язык на какой хочешь переводить", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in lanquages.values())
async def set_language(message: types.Message):
    dest_lang = list(lanquages.keys())[list(lanquages.values()).index(message.text)]
    User.dest_lang = dest_lang
    await message.answer(f"Теперь я буду переводить на {message.text}")


@dp.message_handler()
async def translate_text(message: types.Message):
    src_lang = "ru"
    dest_lang = User.dest_lang

    translated_text = translate(message.text, src_lang, dest_lang)
    await message.answer(translated_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
