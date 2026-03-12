import telebot
from telebot import types
import os

# Mengambil Token dari environment variable agar aman
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Database Sementara (Bisa kita tambah nanti)
database_scam = {
    "investcepat.com": {"laporan": 12, "status": "SCAM", "skor": 90, "server": "Rusia"},
    "profit100x.net": {"laporan": 5, "status": "RISIKO TINGGI", "skor": 75, "server": "Panama"}
}

# --- 1. FITUR START DENGAN TOMBOL ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Membuat rancangan tombol
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🔍 Cek Situs", callback_data='menu_cek')
    btn2 = types.InlineKeyboardButton("🚨 Lapor Situs", callback_data='menu_lapor')
    btn3 = types.InlineKeyboardButton("📚 Panduan Lapor Resmi", callback_data='menu_panduan')
    
    # Menyusun tombol (baris pertama 2 tombol, baris kedua 1 tombol)
    markup.add(btn1, btn2)
    markup.add(btn3)

    teks = (
        "Halo! Selamat datang di *AntiScamGuardBot*! 🛡️\n\n"
        "Saya adalah asisten yang akan melindungimu dari investasi bodong.\n"
        "Silakan pilih menu di bawah ini:"
    )
    bot.reply_to(message, teks, reply_markup=markup, parse_mode='Markdown')

# --- 2. MENGATUR RESPONS KETIKA TOMBOL DITEKAN ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'menu_cek':
        teks = "Untuk mengecek situs (termasuk alamat IP & umur domain), ketik perintah:\n`/cek <link_website>`\n\nContoh: `/cek investcepat.com`"
        bot.send_message(call.message.chat.id, teks, parse_mode='Markdown')
        
    elif call.data == 'menu_lapor':
        teks = "Minta tolong bantuannya! Kirimkan link situs yang dicurigai dengan format:\n`/lapor <link_website>`"
        bot.send_message(call.message.chat.id, teks, parse_mode='Markdown')
        
    elif call.data == 'menu_panduan':
        teks = (
            "📜 *PANDUAN MELAPORKAN SITUS SCAM* 📜\n\n"
            "Jika kamu menjadi korban, segera lapor ke pihak berwenang berikut:\n\n"
            "🏛️ *1. OJK (Satgas PASTI)*\n"
            "WhatsApp: 081-157-157-157\n"
            "Email: konsumen@ojk.go.id\n\n"
            "📈 *2. Bappebti*\n"
            "Website: lapor.bappebti.go.id\n\n"
            "🌐 *3. Kominfo*\n"
            "Website: aduankonten.id\n\n"
            "👮 *4. Polisi Siber*\n"
            "Website: patrolisiber.id"
        )
        bot.send_message(call.message.chat.id, teks, parse_mode='Markdown')

# --- 3. FITUR UTAMA CEK SITUS ---
@bot.message_handler(commands=['cek'])
def cek_situs(message):
    teks_pesan = message.text.split()
    if len(teks_pesan) < 2:
        bot.reply_to(message, "⚠️ Masukkan link! Contoh: `/cek investcepat.com`", parse_mode='Markdown')
        return

    domain = teks_pesan[1].lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]

    if domain in database_scam:
        data = database_scam[domain]
        balasan = (
            "⚠️ *SCAM TERDETEKSI* ⚠️\n\n"
            f"🌐 Domain: `{domain}`\n"
            f"🌍 Server: {data['server']}\n"
            f"🚨 Laporan: {data['laporan']} korban\n"
            f"🔥 Skor Risiko: {data['skor']}%\n"
            f"⚠️ Status: {data['status']}\n\n"
            "Kesimpulan: Bahaya! Jangan setor uang ke sini!"
        )
        bot.reply_to(message, balasan, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"✅ Domain `{domain}` belum ada di database scam kami. Tetap waspada!", parse_mode='Markdown')

# Menjalankan Bot
print("Bot Anti-Scam sudah berjalan...")
bot.polling(none_stop=True)
