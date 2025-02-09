import os
import logging
import asyncio
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TimedOut, NetworkError

# Configura il bot
TOKEN = os.getenv("TOKEN")  # Usa la variabile d'ambiente per il token
WEB_APP_URL = "https://chi-sono.vercel.app"  # Sostituisci con il link della tua Web App
app = Flask(__name__)

# Configura il logging per debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creiamo e inizializziamo l'application PRIMA di usarla
async def create_application():
    application = Application.builder().token(TOKEN).build()
    await application.initialize()
    await application.bot.initialize()
    bot_info = await application.bot.get_me()
    logger.info(f"Bot inizializzato con username: {bot_info.username}")
    return application

# Creiamo l'application sincronicamente per Flask
loop = asyncio.get_event_loop()
application = loop.run_until_complete(create_application())

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto comando /start da {update.effective_user.id}")  

    # Creiamo il pulsante Web App
    keyboard = [[InlineKeyboardButton("Apri Web App", web_app={"url": WEB_APP_URL})]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # Inviamo il pulsante all'utente con timeout
        await update.message.reply_text("Clicca sul pulsante per aprire la Web App:", reply_markup=reply_markup, timeout=15)
    except TimedOut:
        logger.error("Errore: Timeout nella risposta a Telegram.")
    except NetworkError:
        logger.error("Errore di rete. Verifica la connessione.")

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

    try:
        # Processiamo l'update SOLO dopo aver inizializzato il bot
        loop.run_until_complete(application.process_update(update))
    except TimedOut:
        logger.error("Errore: Timeout mentre si processava l'aggiornamento.")
    except NetworkError:
        logger.error("Errore di rete durante il processing dell'update.")

    return "OK", 200

if __name__ == "__main__":
    logger.info("Avvio del bot...")
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url=f"{os.getenv('RENDER_URL')}/{TOKEN}"
    )
