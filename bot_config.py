from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, dotenv_values
from database import Database


load_dotenv()

TOKEN = dotenv_values(".env").get("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
database = Database('d_b.sqlite3')
