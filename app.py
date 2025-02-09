import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Dispatcher, CallbackContext

# Configura il bot
TOKEN = os.getenv("7824647795:AAHdZcio1hc1k7RLEhp8u_vGMp1RAlOieoA")  # Legge il token dalle variabili d'ambiente
WEB_APP_URL = "https://chi-sono.vercel.app"  # Sostituisci con l'URL di Vercel

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Crea il dispatcher per gestire i comandi di Telegram
dispatcher = Dispatcher(bot, None, use_context=True)

# Comando /start
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Apri Mini App", web_app={"url": WEB_APP_URL})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Clicca per aprire l'app:", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
