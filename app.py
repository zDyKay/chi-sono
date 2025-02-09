import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler

# Configura il bot
TOKEN = os.getenv("TOKEN")  # Usa la variabile d'ambiente per il token
app = Flask(__name__)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context):
    await update.message.reply_text("Ciao! Il bot è attivo 🚀")

application.add_handler(CommandHandler("start", start))

@app.route("/", methods=["GET"])
def home():
    return "Bot Telegram attivo!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Riceve gli aggiornamenti da Telegram e li invia al bot"""
    update = Update.de_json(request.get_json(), bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Avvia il Webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url=f"{os.getenv('RENDER_URL')}/{TOKEN}"
    )
