from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from VCBot.handlers import skip_current_song, skip_item
from VCBot.queues import QUEUE, clear_queue

@Client.on_message(command(['skip'], prefixes=f"/"))
async def skip(client, m: Message):
   chat_id = m.chat.id
   if len(m.command) < 2:
      op = await skip_current_song(chat_id)
      if op==0:
         await m.reply("`Heç nə oxunmur`")
      elif op==1:
         await m.reply("`Oxunan mahnı yoxdur, Səsli söhbətdən ayrıldım...`")
      else:
         await m.reply(f"**Növbəti mahnı⏭** \n**🎧 Oxunur** - [{op[0]}] | `{op[2]}`", disable_web_page_preview=True)
   else:
      skip = m.text.split(None, 1)[1]
      OP = "**Aşağıdakı mahnılar növbədən silindi:-**"
      if chat_id in QUEUE:
         items = [int(x) for x in skip.split(" ") if x.isdigit()]
         items.sort(reverse=True)
         for x in items:
            if x==0:
               pass
            else:
               hm = await skip_item(chat_id, x)
               if hm==0:
                  pass
               else:
                  OP = OP + "\n" + f"**#{x}** - {hm}"
         await m.reply(OP)        
      
@Client.on_message(contact_filter & filters.command(['stop', 'end'], prefixes=f"/"))
async def stop(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.leave_group_call(chat_id)
         clear_queue(chat_id)
         await m.reply("**Oxutma dayandırıldı ⏹️**")
      except Exception as e:
         await m.reply(f"**Xəta** \n`{e}`")
   else:
      await m.reply("`Heçnə oxumur`")
   
@Client.on_message(contact_filter & filters.command(['pause'], prefixes=f"/"))
async def pause(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.pause_stream(chat_id)
         await m.reply("**Pauza edildi ⏸️**")
      except Exception as e:
         await m.reply(f"**Xəta** \n`{e}`")
   else:
      await m.reply("`Heçnə oxumur`")
      
@Client.on_message(contact_filter & filters.command(['resume'], prefixes=f"/"))
async def resume(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.resume_stream(chat_id)
         await m.reply("**Davam edilir ▶**")
      except Exception as e:
         await m.reply(f"**Xəta** \n`{e}`")
   else:
      await m.reply("`Heçnə oxumur`")
