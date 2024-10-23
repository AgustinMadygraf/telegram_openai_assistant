"""
handlers.py
Handlers for the bot.
"""

import time
import datetime
from telegram.ext import CallbackContext
from telegram import Update
from openai import OpenAI

from .config import assistant_id, client_api_key
from .utils import get_message_count, update_message_count, save_qa
from .logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

client = OpenAI(api_key=client_api_key)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message to the user."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! Ask me anything."
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Sends a help message to the user."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Just send me a question and I'll try to answer it.",
    )


def get_answer(message_str) -> str:
    """Get answer from assistant with detailed logging."""
    try:
        thread = client.beta.threads.create()
        logger.info(f"Thread created: ID={thread.id}")

        # Enviar el mensaje inicial al hilo
        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=message_str
        )
        logger.info(f"Message sent: ID={message.id}, Content={message_str}")

        # Crear una ejecución (run) del asistente
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )
        logger.info(f"Run started: ID={run.id}, Status={run.status}")

        # Polling para obtener la respuesta
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            logger.info(f"Attempt {attempt}: Run Status={run.status}, Run ID={run.id}")

            # Registrar detalles adicionales si es necesario
            logger.info(f"Run details: {run}")

            if run.status == "completed":
                logger.info(f"Run completed successfully: Run ID={run.id}")
                break

            time.sleep(1)
            attempt += 1

        if attempt == max_attempts:
            logger.error(f"Run did not complete after {max_attempts} attempts: Run ID={run.id}")
            return "Sorry, the response took too long."

        # Obtener los mensajes del hilo
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        if not messages.dict() or not messages.dict().get("data"):
            logger.error("Received empty or invalid response from OpenAI API.")
            return "Sorry, I couldn't get a valid response."

        response = messages.dict()["data"][0]["content"][0]["text"]["value"]
        logger.info(f"Response received: {response}")

        return response

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return "Sorry, an error occurred while retrieving the answer."



async def process_message(update: Update, context: CallbackContext) -> None:
    """Processes a message from the user, gets an answer, and sends it back."""
    message_data = get_message_count()
    count = message_data["count"]
    date = message_data["date"]
    today = str(datetime.date.today())

    if date != today:
        count = 0
    if count >= 100:
        return

    answer = get_answer(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    update_message_count(count + 1)
    save_qa(
        update.effective_user.id,
        update.effective_user.username,
        update.message.text,
        answer,
    )
