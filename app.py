import os
import logging
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configura il bot
TOKEN = os.getenv("TOKEN")  # Usa la variabile d'ambiente per il token
app = Flask(__name__)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Configura il logging per debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto comando /start da {update.effective_user.id}")  # Logga l'ID dell'utente
    await update.message.reply_text("Ciao! Il bot è attivo 🚀")

application.add_handler(CommandHandler("start", start))

@app.route("/", methods=["GET"])
def home():
    return "Bot Telegram attivo!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Riceve gli aggiornamenti da Telegram e li logga"""
    update = Update.de_json(request.get_json(), bot)
    
    # Log per vedere cosa arriva da Telegram
    logger.info(f"Aggiornamento ricevuto: {update.to_dict()}")

    # Eseguiamo il processamento degli aggiornamenti in modo corretto
    asyncio.run(application.process_update(update))

    return "OK", 200

if __name__ == "__main__":
    # Avvia il Webhook senza async
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url=f"{os.getenv('RENDER_URL')}/{TOKEN}"
    )
