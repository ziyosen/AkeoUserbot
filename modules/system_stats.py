from app import app
from pyrogram import filters, enums
import platform
import os
import time
from datetime import datetime

# Fallback jika modules.styles tidak ada
try:
    from modules.styles import result_box
except ImportError:
    def result_box(title, content, icon="📊"):
        return f"{icon} **{title}**\n━━━━━━━━━━━━━━━━━━━━━━━\n{content}"

print("✅ System Stats module loaded!")

START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    """Konversi detik ke format readable (1d 2h 3m 4s)."""
    intervals = [
        ('d', 86400),
        ('h', 3600),
        ('m', 60),
        ('s', 1)
    ]
    parts = []
    for name, sec in intervals:
        val = seconds // sec
        if val:
            seconds %= sec
            parts.append(f"{val}{name}")
    return " ".join(parts) if parts else "0s"

@app.on_message(filters.command("stats", ".") & filters.me)
async def bot_stats(client, message):
    status = await message.edit("📊 **Sedang menghitung data...**")
    
    c = {"total": 0, "groups": 0, "channels": 0, "users": 0, "bots": 0}
    
    async for dialog in client.get_dialogs():
        c["total"] += 1
        dtype = dialog.chat.type
        if dtype in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            c["groups"] += 1
        elif dtype == enums.ChatType.CHANNEL:
            c["channels"] += 1
        elif dtype == enums.ChatType.PRIVATE:
            if dialog.chat.is_bot:
                c["bots"] += 1
            else:
                c["users"] += 1

    uptime = get_readable_time(int(time.time() - START_TIME))
    res = (
        f"⏱️ **Uptime:** `{uptime}`\n"
        f"💬 **Total Chat:** `{c['total']}`\n"
        f"👥 **Grup:** `{c['groups']}`\n"
        f"📢 **Channel:** `{c['channels']}`\n"
        f"👤 **User:** `{c['users']}`\n"
        f"🤖 **Bot:** `{c['bots']}`"
    )
    await status.edit(result_box("STATISTIK AKUN", res, "📊"))

@app.on_message(filters.command("sysinfo", ".") & filters.me)
async def system_info(client, message):
    await message.edit("📡 **Mengambil informasi server...**")
    
    statvfs = os.statvfs('/')
    total = statvfs.f_frsize * statvfs.f_blocks / (1024**3)
    free = statvfs.f_frsize * statvfs.f_bfree / (1024**3)
    used = total - free
    percent = (used / total) * 100
    
    bar_size = 10
    filled = int(percent / 10)
    bar = "■" * filled + "□" * (bar_size - filled)

    res = (
        f"🖥️ **OS:** `{platform.system()} {platform.machine()}`\n"
        f"🐍 **Python:** `{platform.python_version()}`\n"
        f"🏠 **Node:** `{platform.node()}`\n\n"
        f"💾 **Storage:** `{percent:.1f}%`\n"
        f"`[{bar}]`\n"
        f"`{used:.2f}GB / {total:.2f}GB`"
    )
    await message.edit(result_box("SISTEM INFO", res, "💻"))

@app.on_message(filters.command("botinfo", ".") & filters.me)
async def bot_info(client, message):
    me = await client.get_me()
    uptime = get_readable_time(int(time.time() - START_TIME))
    
    try:
        mod_count = len([f for f in os.listdir("modules") if f.endswith('.py')])
    except FileNotFoundError:
        mod_count = 0

    res = (
        f"🤖 **Nama:** {me.first_name}\n"
        f"🆔 **ID:** `{me.id}`\n"
        f"📦 **Modules:** `{mod_count} file`\n"
        f"⏱️ **Uptime:** `{uptime}`\n"
        f"🔗 **User:** @{me.username if me.username else 'N/A'}"
    )
    await message.edit(result_box("BOT INFORMATION", res, "🤖"))
