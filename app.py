import os
import logging
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configura il bot
TOKEN = os.getenv("TOKEN")  # Usa la variabile d'ambiente per il token
app = Flask(__name__)

# Configura il logging per debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creiamo e inizializziamo l'application PRIMA di usarla
async def create_application():
    application = Application.builder().token(TOKEN).build()
    await application.initialize()
    await application.bot.initialize()
    bot_info = await application.bot.get_me()  # Controllo finale per evitare errori
    logger.info(f"Bot inizializzato con username: {bot_info.username}")
    return application

# Creiamo l'application sincronicamente per Flask
loop = asyncio.get_event_loop()
application = loop.run_until_complete(create_application())

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto comando /start da {update.effective_user.id}")  # Logga l'ID dell'utente
    await update.message.reply_text("Ciao! Il bot è attivo 🚀")

# Aggiunge il comando all'application
application.add_handler(CommandHandler("start", start))

@app.route("/", methods=["GET"])
def home():
    return "Bot Telegram attivo!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Riceve gli aggiornamenti da Telegram e li logga"""
    update = Update.de_json(request.get_json(), application.bot)
    
    # Log per vedere cosa arriva da Telegram
    logger.info(f"Aggiornamento ricevuto: {update.to_dict()}")

    # Processiamo l'update SOLO dopo aver inizializzato il bot
    loop.run_until_complete(application.process_update(update))

    return "OK", 200

if __name__ == "__main__":
    logger.info("Avvio del bot...")
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url=f"{os.getenv('RENDER_URL')}/{TOKEN}"
    )

