from app import app
from pyrogram import filters
from pyrogram.types import Message
import os
import time
from PIL import Image

print("✅ Sticker module loaded!")

@app.on_message(filters.command("stiker", ".") & filters.me)
async def to_sticker(client, message: Message):
    msg = message.reply_to_message
    if not msg or not (msg.photo or (msg.document and msg.document.mime_type and "image" in msg.document.mime_type)):
        return await message.edit("❌ Reply ke gambar atau file gambar!")

    if msg.sticker:
        return await message.edit("❌ Ini sudah stiker, Bos!")

    status = await message.edit("🔄 **Memproses stiker...**")
    download_path = None
    stiker_path = f"stiker_{int(time.time())}.webp"

    try:
        download_path = await msg.download()
        img = Image.open(download_path)
        
        # Konversi ke mode RGB/RGBA jika perlu (misal mode P)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        
        # Resize proporsional maksimal 512x512
        img.thumbnail((512, 512))
        img.save(stiker_path, "WEBP")
        
        await client.send_sticker(message.chat.id, stiker_path)
        await status.delete()
        await message.delete()  # hapus perintah
    except Exception as e:
        await status.edit(f"❌ **Error:** `{e}`")
    finally:
        for path in (download_path, stiker_path):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

@app.on_message(filters.command("emoji", ".") & filters.me)
async def text_to_emoji(client, message: Message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.emoji [teks]`")
    
    teks = " ".join(message.command[1:]).lower()
    # Mapping a-z ke regional indicator (lebih ringkas)
    mapping = {chr(ord('a') + i): chr(0x1F1E6 + i) for i in range(26)}
    hasil = "".join(mapping.get(c, c) for c in teks)
    
    if len(hasil) > 4096:
        return await message.edit("❌ Teks terlalu panjang!")
    await message.edit(hasil)
