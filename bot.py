import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.environ.get("TOKEN")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        await update.message.reply_text("Kirim link TikTok / YT / IG ya mas!")
        return
    await update.message.reply_text("Lagi download... tunggu bentar")
    try:
        ydl_opts = {'format': 'best[ext=mp4]/best', 'outtmpl': 'video.%(ext)s', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        await update.message.reply_video(video=open(filename, 'rb'), caption="Nih dari @clipclapku_bot")
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"Gagal mas, coba link lain.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
app.run_polling()
