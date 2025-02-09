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

# Variabile globale per tenere traccia dell'inizializzazione
bot_initialized = False

# Funzione per inizializzare il bot all'avvio
async def initialize_bot():
    global bot_initialized
    if bot_initialized:
        return

    logger.info("Inizializzazione dell'Application e del bot...")
    await application.initialize()  # Assicuriamo che il bot sia completamente pronto
    await application.bot.initialize()  # Forziamo l'inizializzazione del bot

    # Controllo finale per confermare che il bot sia davvero pronto
    bot_info = await application.bot.get_me()
    logger.info(f"Bot inizializzato con username: {bot_info.username}")

    bot_initialized = True  # Ora il bot è pronto

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
    global bot_initialized
    if not bot_initialized:
        logger.info("Il bot non è ancora inizializzato. Attendo l'inizializzazione prima di processare...")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(initialize_bot())  # Sincronizza l'inizializzazione del bot

    # Ora che il bot è inizializzato, possiamo processare gli aggiornamenti
    loop.run_until_complete(application.process_update(update))

    return "OK", 200

if __name__ == "__main__":
    # Inizializza il bot PRIMA di avviare il Webhook
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_bot())

    # Avvia il Webhook senza async
    logger.info("Avvio del bot...")
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url=f"{os.getenv('RENDER_URL')}/{TOKEN}"
    )


