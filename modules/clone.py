from app import app
from pyrogram import filters, enums
from pyrogram.types import Message
import os
import asyncio

# File penyimpanan data asli
DATA_FILE = "data/clone_backup.json"
os.makedirs("data", exist_ok=True)

def load_backup():
    import json
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_backup(data):
    import json
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Daftar blacklist (developer dan user yang dilarang di-clone)
BLACKLIST_USERNAMES = ["Benxx", "bleszh", "AyiinXd", "ayiinxd"]
BLACKLIST_IDS = []

def is_blacklisted(user) -> bool:
    if user.id in BLACKLIST_IDS:
        return True
    if user.username and user.username.lower() in [x.lower() for x in BLACKLIST_USERNAMES]:
        return True
    return False

async def get_full_user(client, user_id):
    """Amil info lengkap user termasuk bio dan foto."""
    try:
        user = await client.get_users(user_id)
        full = await client.get_chat(user.id)
        bio = full.bio if hasattr(full, 'bio') else ""
        return user, bio
    except:
        return None, None

@app.on_message(filters.command("clone", ".") & filters.me)
async def clone_cmd(client: app, message: Message):
    args = message.text.split(maxsplit=1)
    input_args = args[1] if len(args) > 1 else ""

    # Restore
    if input_args == "restore":
        backup = load_backup()
        user_id = str((await client.get_me()).id)
        if user_id not in backup:
            return await message.edit("❌ **Tidak ada data backup.** Belum pernah clone siapa pun.")
        old = backup[user_id]
        status = await message.edit("🔄 **Mengembalikan identitas asli...**")
        try:
            await client.update_profile(
                first_name=old.get("first_name", ""),
                last_name=old.get("last_name", "")
            )
            if old.get("bio"):
                await client.update_profile(bio=old["bio"])
            if old.get("photo_file_id"):
                # Hapus foto saat ini lalu set foto lama (pyrogram tidak bisa langsung set photo dari file_id? kita download dulu)
                # Metode sederhana: download foto dari file_id lalu upload ulang
                photo_path = await client.download_media(old["photo_file_id"])
                if photo_path:
                    await client.set_profile_photo(photo=photo_path)
                    os.remove(photo_path)
            del backup[user_id]
            save_backup(backup)
            await status.edit("✅ **Identitas asli berhasil dikembalikan!**")
        except Exception as e:
            await status.edit(f"❌ Gagal restore: {e}")
        return

    # Dapatkan target user
    target = None
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif input_args:
        try:
            target = await client.get_users(input_args)
        except:
            return await message.edit("❌ User tidak ditemukan.")
    else:
        return await message.edit("❌ **Gunakan:** `.clone @username` atau reply ke user, atau `.clone restore`")

    if is_blacklisted(target):
        return await message.edit("❌ **Tidak dapat mengclone akun ini!** (Dilarang oleh developer)")

    me = await client.get_me()
    if target.id == me.id:
        return await message.edit("❌ **Gak bisa clone diri sendiri, goblok!**")

    # Backup data sendiri
    backup = load_backup()
    my_id = str(me.id)
    if my_id not in backup:
        # Ambil foto profil pertama
        photos = await client.get_profile_photos(me.id, limit=1)
        photo_file_id = photos[0].file_id if photos else None
        # Ambil bio sendiri
        my_full = await client.get_chat(me.id)
        my_bio = my_full.bio if hasattr(my_full, 'bio') else ""
        backup[my_id] = {
            "first_name": me.first_name,
            "last_name": me.last_name or "",
            "bio": my_bio,
            "photo_file_id": photo_file_id
        }
        save_backup(backup)

    status = await message.edit(f"🎭 **Mengkloning identitas {target.first_name}...**")

    # Ambil data target
    target_user, target_bio = await get_full_user(client, target.id)
    if not target_user:
        return await status.edit("❌ Gagal mengambil data target.")

    target_first = target_user.first_name or "No Name"
    target_last = target_user.last_name or ""
    target_photo = None
    try:
        photos = await client.get_profile_photos(target.id, limit=1)
        if photos:
            target_photo = photos[0].file_id
    except:
        pass

    # Update profil
    try:
        await client.update_profile(first_name=target_first, last_name=target_last)
        if target_bio:
            await client.update_profile(bio=target_bio)
        if target_photo:
            # Download foto target dan upload ke profil
            photo_path = await client.download_media(target_photo)
            if photo_path:
                await client.set_profile_photo(photo=photo_path)
                os.remove(photo_path)
        await status.edit(f"✅ **Berhasil mengkloning {target_user.first_name}!**\nGunakan `.clone restore` untuk kembali.")
    except Exception as e:
        await status.edit(f"❌ Gagal clone: {e}")
