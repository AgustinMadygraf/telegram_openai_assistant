"""
utils.py
This file contains utility functions for the Telegram bot.
"""

import json
from pathlib import Path
import datetime
from .logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

# Paths to the files
message_count_file = Path("C:/AppServ/www/telegram_openai_assistant/message_count.json")
qa_file = Path("C:/AppServ/www/telegram_openai_assistant/questions_answers.json")

def get_message_count():
    """Retrieve the current message count."""
    if not message_count_file.exists():
        return {"date": str(datetime.date.today()), "count": 0}
    with open(message_count_file) as file:
        return json.load(file)

def update_message_count(new_count):
    """Update the message count in the file."""
    try:
        with open(message_count_file, 'w') as file:
            json.dump({"date": str(datetime.date.today()), "count": new_count}, file)
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def save_qa(telegram_id, username, question, answer):
    """Save question and answer pairs to a file along with user information."""
    try:
        with open(qa_file, 'r+') as file:
            data = json.load(file)
            data.append({
                "telegram_id": telegram_id,
                "username": username,
                "question": question,
                "answer": answer
            })
            file.seek(0)
            json.dump(data, file, indent=4)
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
