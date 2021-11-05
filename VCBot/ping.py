import os
import sys
import asyncio
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from time import time
from datetime import datetime

# System Uptime
START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ('Week', 60 * 60 * 24 * 7),
    ('Day', 60 * 60 * 24),
    ('Hour', 60 * 60),
    ('Min', 60),
    ('Sec', 1)
)
async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(contact_filter & filters.command(['ping'], prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
   start = time()
   current_time = datetime.utcnow()
   m_reply = await m.reply_text("`...`")
   delta_ping = time() - start
   uptime_sec = (current_time - START_TIME).total_seconds()
   uptime = await _human_time_duration(int(uptime_sec))
   await m_reply.edit(f"`{delta_ping * 1000:.3f} ms` \n**Uptime ⏳** - `{uptime}`")

@Client.on_message(contact_filter & filters.command(['restart'], prefixes=f"{HNDLR}"))
async def restart(client, m: Message):
   await m.reply("`Yenidən başladıldı.Xətalar düzəldildi.`")
   os.execl(sys.executable, sys.executable, *sys.argv)
   # You probably don't need it but whatever
   quit()

@Client.on_message(contact_filter & filters.command(['start'], prefixes=f"/"))
async def help(client, m: Message):
   HELP = f"**işləmə qaydası 🛠** \n\n__Adi istifadəçi əmrləri__ (👑): \n`/play mahnı adı yazın` \n`/kanal [kanal linki] ; [n]` - kanaldan mahnı seçərək səsləndirər \n`/siyahi` / `/playlist növbədə olan mahnı siyahısını göstərər` \n\n__Admin əmrləri__ (İşləməsi üçün userbotun kontaktınaa əlavə edilin): \n`/ping botun pingini göstərər` \n`/skip növbəti mahnıya keçid edər` \n`/pause mahnını dayandırar` və `/resume mahnını davam etdirər` \n`/stop Oxutmanı sonlandırar` / `/end oxutmanı sonlandırar` \n`/start kömək menyusunu açar` \n`!restart botu yenidən başladar`"
   await m.reply(HELP)
