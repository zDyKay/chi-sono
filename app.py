from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext, Dispatcher

TOKEN = "7824647795:AAHdZcio1hc1k7RLEhp8u_vGMp1RAlOieoA"
WEB_APP_URL = "https://ChiChiamo.vercel.app"

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, use_context=True)

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Apri Mini App", web_app=WEB_APP_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Clicca per aprire l'app:", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
