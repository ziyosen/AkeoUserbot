from app import app
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import YouBlockedUser
import os
import asyncio

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.on_message(filters.command("kamuii", ".") & filters.me)
async def deepfry_cmd(client, message: Message):
    # Cek apakah ada reply
    replied = message.reply_to_message
    if not replied:
        return await message.edit("❌ Balas ke foto atau stiker!")
    
    # Cek media
    if not (replied.photo or replied.sticker):
        return await message.edit("❌ Hanya foto atau stiker yang bisa di-deepfry!")
    
    # Ambil level (1-8)
    level = None
    if len(message.command) > 1:
        try:
            level = int(message.command[1])
            if not 1 <= level <= 8:
                level = None
        except:
            pass
    
    status = await message.edit("🔄 **Mengirim media ke bot deepfry...**")
    
    # Kirim ke bot
    bot_username = "image_deepfry_bot"
    try:
        async with client.conversation(bot_username, timeout=60) as conv:
            # Kirim media (foto atau stiker)
            if replied.photo:
                await conv.send_photo(replied.photo.file_id)
            else:
                await conv.send_sticker(replied.sticker.file_id)
            
            # Jika ada level, kirim perintah
            if level:
                await conv.send_message(f"/deepfry {level}")
            
            # Ambil respons (hasil deepfry)
            response = await conv.get_response()
            # Mungkin bot mengirim teks dulu, loop sampai dapat media
            while not (response.photo or response.sticker or response.document):
                response = await conv.get_response()
            
            # Download media hasil
            file_path = await client.download_media(response, file_name=os.path.join(TEMP_DIR, "deepfry_result.jpg"))
            if not file_path:
                await status.edit("❌ Gagal mengunduh hasil deepfry.")
                return
            
            # Kirim balik ke chat (sebagai foto)
            await client.send_photo(
                message.chat.id,
                file_path,
                reply_to_message_id=replied.id,
                caption=f"🍟 Hasil deepfry {f'(level {level})' if level else ''}"
            )
            await status.delete()
            await message.delete()
            
            # Hapus file temporary
            os.remove(file_path)
    
    except YouBlockedUser:
        await status.edit(f"❌ Anda memblokir @{bot_username}. Buka blokir dulu.")
    except Exception as e:
        await status.edit(f"❌ Error: `{e}`")
