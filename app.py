import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler

# Configura il bot
TOKEN = os.getenv("TOKEN")  # Legge il token dalle variabili d'ambiente
WEB_APP_URL = "https://your-web-app.vercel.app"  # Sostituisci con l'URL di Vercel

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Apri Mini App", web_app={"url": WEB_APP_URL})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Clicca per aprire l'app:", reply_markup=reply_markup)

application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Riceve gli aggiornamenti da Telegram e li invia al bot"""
    update = Update.de_json(request.get_json(), bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

if __name__ == "__main__":
    application.run_polling()
