import os
import json
import pytesseract
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from PIL import Image
import io

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

ARCHIVE_FILE = "archive.json"

def save_to_archive(user_id, file_name, text):
    entry = {
        "user_id": user_id,
        "file_name": file_name,
        "text": text
    }
    if os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Привет! Я — ПолимахБот. Отправь фото или PDF документа, чтобы я распознал текст.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await photo.download(destination=io.BytesIO())
    file.seek(0)
    image = Image.open(file)
    text = pytesseract.image_to_string(image, lang="rus+eng")
    save_to_archive(message.from_user.id, "photo.jpg", text)
    preview = text[:1000]
    await message.reply("Текст распознан. Вот начало:

" + preview)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
