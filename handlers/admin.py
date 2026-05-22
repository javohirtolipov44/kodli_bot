import asyncio
import time
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from baza.homiy import add_homiy, del_homiy, get_all_homiy
from baza.users import get_users_count, get_all_users
from baza.chanel import get_chanel, add_chanel, del_chanel, get_all_chanels
from config import ADMINS
from keyboards.admin import admin_kb
from keyboards.message import message_kb
from keyboards.homiy import homiy_kb
from keyboards.anime import anime_kb
from states.homiy_state import HomiyState
from states.admin_state import AdminState
from states.anime_chanel_state import AnimeChanelState

router = Router()

@router.message(F.text.startswith("/admin"))
async def admin(message: Message, state: FSMContext):
    if not message.from_user.id in ADMINS:
        await message.answer("Siz admin emassiz")
        return
    await state.clear()
    await message.answer("Admin panelga xush kelibsiz!!!", reply_markup=admin_kb)

@router.callback_query(F.data == "statistika")
async def statistika(callback: CallbackQuery):
    if not callback.from_user.id in ADMINS:
        await callback.answer("Siz admin emassiz")
        return
    user = await get_users_count()
    await callback.message.edit_text(f"Barcha obunachilar: {user}", reply_markup=admin_kb)

@router.callback_query(F.data == "send_message")
async def send_message(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user.id in ADMINS:
        await callback.answer("Siz admin emassiz")
        return
    await state.set_state(AdminState.send_message)
    await callback.message.edit_text("Xabaringizni yuboring")

@router.message(AdminState.send_message)
async def send_message_finish(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    await state.update_data(
    from_chat_id=message.chat.id,
    message_id=message.message_id
)
    await message.answer("Xabar tasdiqlandi yuboraymi?", reply_markup=message_kb)

@router.callback_query(F.data == "send")
async def confirm_broadcast(
    call: CallbackQuery,
    state: FSMContext,
    bot: Bot
):
    if call.from_user.id not in ADMINS:
        return

    data = await state.get_data()
    from_chat_id = data.get("from_chat_id")
    message_id = data.get("message_id")

    

    user_ids = await get_all_users()  # PostgreSQL async

    await call.message.edit_text(
        f"⏳ Xabar yuborilmoqda...\n"
        f"👥 Foydalanuvchilar: {len(user_ids)}"
    )

    # 🔥 ASOSIY JOY
    asyncio.create_task(
        broadcast_copy(bot, from_chat_id, message_id, user_ids)
    )

    await call.answer("🚀 Broadcast boshlandi")
    await state.clear()

async def broadcast_copy(bot: Bot, from_chat, msg_id, users):
    start_time = time.monotonic()   # ⏱ boshlanish vaqti
    success = 0
    failed = 0

    total = len(users)

    for i, user_id in enumerate(users, start=1):
        
        try:
            await bot.copy_message(user_id, from_chat, msg_id)
            success += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await bot.copy_message(user_id, from_chat, msg_id)
                success += 1
            except:
                failed += 1
        except TelegramForbiddenError:
            failed += 1
        except Exception as e:
            failed += 1
            print(f"Xato {user_id}: {e}")

        await asyncio.sleep(0.05)  # ⚡ tez, xavfsiz

    # ⏱ tugash vaqti
    elapsed = time.monotonic() - start_time

    minutes, seconds = divmod(int(elapsed), 60)

    report = (
        "✅ Broadcast yakunlandi\n\n"
        f"👥 Jami foydalanuvchilar: {total}\n"
        f"📬 Yuborildi: {success}\n"
        f"❌ Xatolik: {failed}\n"
        f"⏱ Sarflangan vaqt: {minutes} daqiqa {seconds} soniya"
    )

    # 📣 Admin(lar)ga xabar berish
    await bot.send_message(from_chat, report)

@router.callback_query(F.data == "anime_chanel")
async def anime_chanel(callback: CallbackQuery):
    if not callback.from_user.id in ADMINS:
        await callback.answer("Siz admin emassiz")
        return
    await callback.message.edit_text("Anime kanallarni sozlash", reply_markup=anime_kb)

@router.message(F.forward_from_chat, AnimeChanelState.id) 
async def handle_forwarded(message: Message, state: FSMContext):
    original_chat = message.forward_from_chat  
    chanel_id = original_chat.id
    title = original_chat.title
    chanel = await get_chanel(chanel_id)
    if chanel:
        await message.answer(f"Bu kanal allaqachon bazada mavjud: {title}\n (ID: {chanel_id})")
        await state.clear()
        return
    await add_chanel(chanel_id, title)
    await message.answer(
        f"Kanal saqlandi!\n"
        f"Kanal IDsi: {chanel_id}\n"
        f"Kanal nomi: {title}")
    await message.answer("Admin panelga xush kelibsiz!!!", reply_markup=admin_kb)
    await state.clear()

@router.message(F.forward_from_chat, AnimeChanelState.del_id) 
async def handle_forwarded(message: Message, state: FSMContext):
    original_chat = message.forward_from_chat  
    chanel_id = original_chat.id
    title = original_chat.title
    chanel = await get_chanel(chanel_id)
    if not chanel:
        await message.answer(f"Bu kanal bazada mavjud emas: {title}\n (ID: {chanel_id})")
        await state.clear()
        return
    await del_chanel(chanel_id)
    await message.answer(
        f"Kanal o'chirildi!\n"
        f"Kanal IDsi: {chanel_id}\n"
        f"Kanal nomi: {title}")
    await message.answer("Admin panelga xush kelibsiz!!!", reply_markup=admin_kb)
    await state.clear()

@router.callback_query(F.data == "anime_chanel_add")
async def anime_chanel_add(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user.id in ADMINS:
        await callback.message.answer("Siz admin emassiz")
        return
    await callback.message.edit_text("Kanaldagi biror postni forward qiling")
    await state.set_state(AnimeChanelState.id)

@router.callback_query(F.data == "anime_chanel_del")
async def anime_chanel_del(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user.id in ADMINS:
        await callback.message.answer("Siz admin emassiz")
        return
    await callback.message.edit_text("Kanaldagi biror postni forward qiling")
    await state.set_state(AnimeChanelState.del_id)

@router.callback_query(F.data == "homiy_chanel")
async def homiy_chanel(callback: CallbackQuery):
    if not callback.from_user.id in ADMINS:
        await callback.answer("Siz admin emassiz")
        return
    await callback.message.edit_text("Homiy kanallarni sozlash", reply_markup=homiy_kb)

@router.callback_query(F.data == "homiy_add")
async def homiy_add_id(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user.id in ADMINS:
        await callback.message.answer("Siz admin emassiz")
        return
    await callback.message.edit_text("Kanal id sini yuboring masalan: -1001886333433")
    await state.set_state(HomiyState.id)

@router.message(HomiyState.id)
async def homiy_add_link(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    await state.update_data(id = message.text)
    await message.answer(f"ID qabul qilindi: {message.text}\n"
                         f"Kanal havolasini yuboring masalan: https://t.me/animeprofessional", disable_web_page_preview=True)
    await state.set_state(HomiyState.link)

@router.message(HomiyState.link)
async def homiy_add_finish(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    data = await state.get_data()
    await message.answer("✅ Kanal muvaffaqiyatli qo‘shildi\n"
        "Admin panel orqali uni boshqarishingiz mumkin.")
    await add_homiy(data["id"],message.text)
    await state.clear()
    await message.answer("Admin panel", reply_markup=admin_kb)

@router.callback_query(F.data == "homiy_del")
async def homiy_del_id(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user.id in ADMINS:
        await callback.message.answer("Siz admin emassiz")
        return
    await callback.message.edit_text("Kanal id sini yuboring masalan: -100123456789")
    await state.set_state(HomiyState.del_id)

@router.message(HomiyState.del_id)
async def homiy_add_finish(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    if await del_homiy(message.text):
        await message.answer("Homiy kanal malumotlar bazasidan o'chirildi")
    else:
        await message.answer("Bunday ID mavjud emas")
    await state.clear()
    await message.answer("Admin panelga xush kelibsiz!!!", reply_markup=admin_kb)

@router.callback_query(F.data == "homiy_list")
async def homiy_list(callback: CallbackQuery):
    if not callback.from_user.id in ADMINS:
        await callback.answer("Siz admin emassiz")
        return
    homiylar = await get_all_homiy()
    text = "📢 Homiy kanallar ro‘yxati:\n\n"
    i = 1
    for h in homiylar:
        # h = (id, chanel_id, link)
        text += f"🔗 №: {i}\n"
        text += f"🆔 Chanel ID: {h[1]}\n"
        text += f"🌐 Link: {h[2]}\n\n"
        i+=1

    await callback.message.edit_text(text, disable_web_page_preview=True)
    await callback.message.answer("Admin panelga xush kelibsiz!!!", reply_markup=admin_kb)

@router.callback_query(F.data == "anime_chanel_list")
async def anime_chanel_list(callback: CallbackQuery):
    if not callback.from_user.id in ADMINS:
        await callback.answer("Siz admin emassiz")
        return
    chanels = await get_all_chanels()
    text = "📢 Homiy kanallar ro‘yxati:\n\n"
    i = 1
    for h in chanels:
        # h = (id, chanel_id, link)
        text += f"🔗 №: {i}\n"
        text += f"🆔 Chanel ID: {h[1]}\n"
        text += f"🌐 Nomi: {h[2]}\n\n"
        i+=1

    await callback.message.edit_text(text, disable_web_page_preview=True)
    await callback.message.answer("Admin panelga xush kelibsiz!!!", reply_markup=admin_kb)

