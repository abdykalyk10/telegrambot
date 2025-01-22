from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from database import Database
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
database = Database('d_b.sqlite3')
