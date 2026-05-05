from app import app
from pyrogram import filters
from pyrogram.types import Message
import os
import time
from PIL import Image

print("✅ Sticker module loaded!")

@app.on_message(filters.command("stiker", ".") & filters.me)
async def to_sticker(client, message: Message):
    # Logika: Satukan pengecekan gambar & dokumen
    msg = message.reply_to_message
    if not msg or not (msg.photo or (msg.document and "image" in msg.document.mime_type)):
        return await message.edit("❌ Reply ke gambar atau foto dokument!")

    if msg.sticker:
        return await message.edit("❌ Ini sudah stiker, Bos!")

    status = await message.edit("🔄 **Sedang memproses stiker...**")
    
    # Lokasi file sementara
    download_path = await msg.download()
    stiker_path = f"stiker_{int(time.time())}.webp"

    try:
        # Logika Pengolahan Gambar
        img = Image.open(download_path)
        
        # Biar stiker proposional dan masuk standar Telegram (512x512)
        img.thumbnail((512, 512))
        
        # Simpan ke format WebP
        img.save(stiker_path, "WEBP")

        # Kirim
        await client.send_sticker(message.chat.id, stiker_path)
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ **Error:** `{e}`")
    
    finally:
        # Logika Pembersihan: Apapun yang terjadi, hapus file sisa
        if os.path.exists(download_path):
            os.remove(download_path)
        if os.path.exists(stiker_path):
            os.remove(stiker_path)

@app.on_message(filters.command("emoji", ".") & filters.me)
async def text_to_emoji(client, message: Message):
    if len(message.command) < 2:
        return await message.edit("❌ Gunakan: `.emoji [teks]`")

    teks = " ".join(message.command[1:]).lower()
    
    # Mapping regional indicator symbols
    # Logika: Menggunakan base offset untuk menghemat baris kode
    mapping = {
        'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪',
        'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯',
        'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴',
        'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
        'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾',
        'z': '🇿'
    }
    
    hasil = "".join([mapping.get(c, c) for c in teks])
    
    # Logika: Jika hasil terlalu panjang, Telegram akan error. 
    if len(hasil) > 4096:
        return await message.edit("❌ Teks terlalu panjang!")
        
    await message.edit(hasil)
