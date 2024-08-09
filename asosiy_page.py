import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from telethon import TelegramClient
from config import BOT_TOKEN, YOUR_ADMIN_ID
import sqlite3
API_TOKEN = BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


api_id = '28312933'
api_hash = '1f75793fc211a5eb3812a860cfe6c713'
phone_number = '+998883601656'
# Telethon Client
client = TelegramClient('session_name', api_id, api_hash)

async def start_telethon_client():
    await client.start(phone_number)


class Form(StatesGroup):
    adding_group = State()

class Form1(StatesGroup):
    sending_post = State()

@dp.message(Command('start'))
async def CommandStart(message: types.Message):
    await message.answer(f"")





@dp.message(Command(commands=["guruh"]))
async def ask_for_group_link(message: types.Message, state: FSMContext):
    if message.from_user.id != YOUR_ADMIN_ID:
        await message.answer("Sizda bu komanda uchun ruxsat yo'q.")
        return

    await message.answer("Guruh linklarini yuboring:")
    await state.set_state(Form.adding_group)


@dp.message(Form.adding_group)
async def add_group_link(message: types.Message, state: FSMContext):
    links = message.text.split('\n')
    added_links = 0
    for link in links:
        link = link.strip()
        if link.startswith("https://t.me/"):
            if add_data(link):
                added_links += 1
        else:
            await message.answer(f"Noto'g'ri formatda link yuborildi: {link}. To'g'ri formatda link yuboring.")

    if added_links > 0:
        await message.answer(f"{added_links} ta link ma'lumotlar bazasiga qo'shildi.")
    else:
        await message.answer("Hech qanday to'g'ri link topilmadi.")

    await message.answer(
        "Yana guruh linklarini yuborishingiz mumkin yoki /send komandasi orqali xabar yuborishingiz mumkin.")
    await state.clear()


@dp.message(Command(commands=["send"]))
async def ask_for_post(message: types.Message, state: FSMContext):
    if message.from_user.id != YOUR_ADMIN_ID:
        await message.answer("Sizda bu komanda uchun ruxsat yo'q.")
        return

    await message.answer("Yuboradigan postni yuboring:")
    await state.set_state(Form1.sending_post)

@dp.message(Form1.sending_post)
async def send_to_groups(message: types.Message, state: FSMContext):
    all_links = get_all_links()

    if not all_links:
        await message.answer("Ma'lumotlar bazasida hech qanday guruh linki topilmadi.")
        return

    async with client:
        for (link,) in all_links:
            try:
                entity = await client.get_entity(link)
                if message.content_type == 'text':
                    await client.send_message(entity, message.text)
                elif message.photo:
                    await client.send_file(entity, await message.photo[-1].download(), caption=message.caption)
                elif message.video:
                    await client.send_file(entity, await message.video.download(), caption=message.caption)
                elif message.document:
                    await client.send_file(entity, await message.document.download(), caption=message.caption)
                await message.answer(f"Xabar {link} ga yuborildi.")
            except Exception as e:
                await message.answer(f"Xabar {link} ga yuborishda xato: {e}")
                logging.error(f"Xato yuz berdi: {e}")

    await state.clear()

def add_data(link):
    try:
        cursor.execute('INSERT INTO my_table (link) VALUES (?)', (link,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_all_links():
    cursor.execute('SELECT link FROM my_table')
    return cursor.fetchall()

async def main():
    logging.basicConfig(level=logging.INFO)

    global conn, cursor
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY,
        link TEXT NOT NULL UNIQUE
    )
    ''')

    await start_telethon_client()
    await dp.start_polling(bot, skip_updates=True)

    conn.close()

if __name__ == '__main__':
    asyncio.run(main())
