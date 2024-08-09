from telethon import TelegramClient, events, sync

# API ID va Hash o'rniga o'zingizning qiymatlarni qo'ying
api_id = '28312933'
api_hash = '1f75793fc211a5eb3812a860cfe6c713'
phone_number = '+998883601656'  # Sizning telefon raqamingiz (Telegram'da ro'yxatdan o'tgan)


# TelegramClient ob'ektini yarating
client = TelegramClient('session_name', api_id, api_hash)

# Mijozni ishga tushiring
client.start(phone_number)

# /start komandasiga javob berish
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply('Salom! Men sizning Telegram botingizman!')

# Guruhga xabar yuborish funksiyasi
@client.on(events.NewMessage(pattern='/sendto (\S+) (.*)'))
async def send_message_to(event):
    # Guruh yoki foydalanuvchi ID sini olish
    target = event.pattern_match.group(1)
    # Xabar matnini olish
    message_text = event.pattern_match.group(2)
    # Xabar yuborish
    await client.send_message(target, message_text)


# Media fayllarni yuborish funksiyasi
@client.on(events.NewMessage(pattern='/sendmedia (\S+) (\S+)'))
async def send_media(event):
    target = event.pattern_match.group(1)
    file_path = event.pattern_match.group(2)
    await client.send_file(target, file_path)


# Mijozni doimiy ravishda ishlashiga ruxsat berish
client.run_until_disconnected()