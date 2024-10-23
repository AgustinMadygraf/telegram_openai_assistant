"""
config.py
Configuration file for the bot.
"""
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file.
load_dotenv()

# Retrieve the variables from the environment.
assistant_id = os.getenv("ASSISTANT_ID")
client_api_key = os.getenv("CLIENT_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")
