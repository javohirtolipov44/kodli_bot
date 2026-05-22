from aiogram import Router, F
from aiogram.types import Message
import string, random
from baza.chanel import get_chanel
from config import BOT_URL
from baza.anime import add_anime

router = Router()

def generate_hash(length=12):
    chars = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choice(chars) for _ in range(length))

@router.channel_post(F.text == "id")
async def id_message(message: Message):
    await message.answer(f"Kanal id raqami: {message.chat.id}")
    if message.chat.username:
       await message.answer(f"https://t.me/{message.chat.username}")

@router.channel_post()
async def all_message(message: Message):
    chanel_id = message.chat.id
    m_id = message.message_id
    title = message.chat.title
    chanel = await get_chanel(chanel_id)
    if not chanel:
        return
    unique_hash = generate_hash()
    try:
        await add_anime(chanel_id, m_id, title, unique_hash)
        await message.reply(f"https://t.me/{BOT_URL}?start={unique_hash}")
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}\n Qayta urinib ko'ring.")
    