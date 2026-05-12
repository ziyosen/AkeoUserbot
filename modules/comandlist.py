from app import app
from pyrogram import filters

@app.on_message(filters.command(["commandlist", "commands"], ".") & filters.me)
async def show_all_commands(client, message):
    text = (
        "<b>📋 Comand List Userbot</b>\n"
        "<i>Prefix: . (titik)</i>\n\n"
        
        "<b>👑 ADMIN & MODERASI</b>\n"
        "• <code>.adminlist</code> - Daftar admin grup\n"
        "• <code>.ban</code> &lt;user&gt; - Ban user\n"
        "• <code>.kick</code> &lt;user&gt; - Kick user\n"
        "• <code>.unban</code> &lt;user&gt; - Unban user\n"
        "• <code>.mute</code> (reply) - Bisukan user\n"
        "• <code>.unmute</code> (reply) - Aktifkan bicara\n"
        "• <code>.promote</code> (reply) - Promosikan jadi admin\n"
        "• <code>.demote</code> (reply) - Turunkan admin\n"
        "• <code>.purge</code> (reply awal) - Hapus banyak pesan\n"
        "• <code>.del</code> (reply) - Hapus satu pesan\n\n"
        
        
        "<b>🔇 AFK MODE</b>\n"
        "• <code>.afk</code> [alasan] (reply media) - Aktifkan AFK\n"
        "• (kirim pesan apapun) - Nonaktifkan AFK\n\n"
        
        "<b>📣 TAG ALL</b>\n"
        "• <code>.mention</code> [teks] - Tag dengan @all\n"
        "• <code>.tagall</code> [teks] - Tag semua dengan nama\n"
        "• <code>.emojitag</code> [teks] - Tag dengan emoji random\n"
        "• <code>.stop</code> - Hentikan proses tag\n\n"
        
        "<b>🎨 MEDIA & STIKER</b>\n"
        "• <code>.stiker</code> (reply foto) - Foto jadi stiker\n"
        "• <code>.emoji</code> &lt;teks&gt; - Teks ke emoji regional\n"
        "• <code>.kamuii</code> (reply) &lt;1-8&gt; - Deepfry gambar\n\n"
        
        
        "<b>📊 INFORMASI</b>\n"
        "• <code>.ping</code> - Cek latency\n"
        "• <code>.alive</code> - Status bot & uptime\n"
        "• <code>.stats</code> - Statistik akun\n"
        "• <code>.sysinfo</code> - Informasi sistem\n"
        "• <code>.botinfo</code> - Info userbot\n"
        "• <code>.id</code> - ID chat / user\n"
        "• <code>.whois</code> &lt;user&gt; - Detail user\n"
        "• <code>.info</code> - Info grup saat ini\n\n"
        
        "<b>🔍 OSINT</b>\n"
        "• <code>.myip</code> - IP publik sendiri\n"
        "• <code>.ip</code> &lt;IP&gt; - Info IP (lokasi, ISP)\n"
        "• <code>.ipsakti</code> &lt;IP&gt; - Info IP lengkap + koordinat\n"
        "• <code>.cekno</code> &lt;nomor&gt; - Cek operator Indonesia\n"
        "• <code>.finduser</code> &lt;username&gt; - Cari di sosmed\n\n"
        
        "<b>😄 HIBURAN</b>\n"
        "• <code>.absen</code> - Pesan hadir random\n"
        "• <code>.aku_ganteng</code> - Pujian narsis\n"
        "• <code>.teemo</code> - Teemo\n"
        "• <code>.give</code> - Giveaway\n"
        "• <code>.uno</code> - Uno\n\n"
        
        "<b>🎭 CLONE IDENTITAS</b>\n"
        "• <code>.clone</code> &lt;user&gt; - Kloning profil target\n"
        "• <code>.clone restore</code> - Kembalikan profil asli\n\n"
        
        "<b>📥 DOWNLOADER</b>\n"
        "• <code>.yt</code> &lt;url&gt; - Download video YouTube (MP4)\n"
        "• <code>.yta</code> &lt;url&gt; - Download audio YouTube (MP3)\n\n"
        
        "👨‍💻 <b>Developer:</b> <a href='https://t.me/Bleszh'>Benxx</a>\n"
    await message.edit(text, disable_web_page_preview=True)
