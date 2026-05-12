from app import app
from pyrogram import filters

@app.on_message(filters.command(["commandlist", "commands"], ".") & filters.me)
async def show_all_commands(client, message):
    text = """
<b>📋 Command List Userbot</b>
<i>Prefix: . (titik)</i>

<b>👑 ADMIN & MODERASI</b>
• <code>.adminlist</code> - Daftar admin grup
• <code>.ban</code> &lt;user&gt; - Ban user
• <code>.kick</code> &lt;user&gt; - Kick user
• <code>.unban</code> &lt;user&gt; - Unban user
• <code>.mute</code> (reply) - Bisukan user
• <code>.unmute</code> (reply) - Aktifkan bicara
• <code>.promote</code> (reply) - Promosikan jadi admin
• <code>.demote</code> (reply) - Turunkan admin
• <code>.purge</code> (reply awal) - Hapus banyak pesan
• <code>.del</code> (reply) - Hapus satu pesan

<b>🔇 AFK MODE</b>
• <code>.afk</code> [alasan] (reply media) - Aktifkan AFK
• (kirim pesan apapun) - Nonaktifkan AFK

<b>📣 TAG ALL</b>
• <code>.mention</code> [teks] - Tag dengan @all
• <code>.tagall</code> [teks] - Tag semua dengan nama
• <code>.emojitag</code> [teks] - Tag dengan emoji random
• <code>.stop</code> - Hentikan proses tag

<b>🎨 MEDIA & STIKER</b>
• <code>.stiker</code> (reply foto) - Foto jadi stiker
• <code>.emoji</code> &lt;teks&gt; - Teks ke emoji regional
• <code>.kamuii</code> (reply) &lt;1-8&gt; - Deepfry gambar

<b>📊 INFORMASI</b>
• <code>.ping</code> - Cek latency
• <code>.alive</code> - Status bot & uptime
• <code>.stats</code> - Statistik akun
• <code>.sysinfo</code> - Informasi sistem
• <code>.botinfo</code> - Info userbot
• <code>.id</code> - ID chat / user
• <code>.whois</code> &lt;user&gt; - Detail user
• <code>.info</code> - Info grup saat ini

<b>🔍 OSINT</b>
• <code>.myip</code> - IP publik sendiri
• <code>.ip</code> &lt;IP&gt; - Info IP (lokasi, ISP)
• <code>.ipsakti</code> &lt;IP&gt; - Info IP lengkap + koordinat
• <code>.cekno</code> &lt;nomor&gt; - Cek operator Indonesia
• <code>.finduser</code> &lt;username&gt; - Cari di sosmed

<b>😄 HIBURAN</b>
• <code>.absen</code> - Pesan hadir random
• <code>.aku_ganteng</code> - Pujian narsis
• <code>.teemo</code> - Teemo
• <code>.give</code> - Giveaway
• <code>.uno</code> - Uno

<b>🎭 CLONE IDENTITAS</b>
• <code>.clone</code> &lt;user&gt; - Kloning profil target
• <code>.clone restore</code> - Kembalikan profil asli

<b>📥 DOWNLOADER</b>
• <code>.yt</code> &lt;url&gt; - Download video YouTube (MP4)
• <code>.yta</code> &lt;url&gt; - Download audio YouTube (MP3)

👨‍💻 <b>Developer:</b> <a href='https://t.me/Bleszh'>Benxx</a>
"""
    await message.edit(text, disable_web_page_preview=True)
