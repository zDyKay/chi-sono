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

# Creiamo l'applicazione di Telegram
application = Application.builder().token(TOKEN).build()

# Configura il logging per debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Funzione per inizializzare il bot all'avvio
async def initialize_bot():
    logger.info("Inizializzazione dell'Application e del bot...")
    await application.initialize()  # Assicuriamo che il bot sia completamente pronto
    await application.bot.initialize()  # Forziamo l'inizializzazione del bot
    logger.info(f"Bot inizializzato con username: {application.bot.username}")

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
    update = Update.de_json(request.get_json(), bot)
    
    # Log per vedere cosa arriva da Telegram
    logger.info(f"Aggiornamento ricevuto: {update.to_dict()}")

    # Assicuriamoci che il bot sia stato inizializzato
    if not application.running:
        logger.info("Il bot non è ancora inizializzato. Inizializzazione in corso...")
        asyncio.run(initialize_bot())  # Inizializza il bot PRIMA di processare gli update

    # Processiamo l'update SOLO dopo aver inizializzato il bot
    asyncio.run(application.process_update(update))

    return "OK", 200

if __name__ == "__main__":
    # Inizializza il bot PRIMA di avviare il Webhook
    asyncio.run(initialize_bot())

    # Avvia il Webhook senza async
    logger.info("Avvio del bot...")
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url=f"{os.getenv('RENDER_URL')}/{TOKEN}"
    )
