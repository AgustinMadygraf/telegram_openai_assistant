"""
run.py
Entry point for the bot.
"""

import os
from src.bot import main

if __name__ == "__main__":
    #limpiar pantalla
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
