"""
bot.py
Entry point for the bot.
"""
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .config import telegram_token
from .handlers import start, help_command, process_message
from .logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")

application = Application.builder().token(telegram_token).build()

def setup_handlers(app):
    """Sets up the command and message handlers for the bot."""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

def main():
    """Main function to run the bot."""
    print("Starting the bot...")
    setup_handlers(application)
    print("Polling for messages...")
    application.run_polling()

if __name__ == "__main__":
    main()
