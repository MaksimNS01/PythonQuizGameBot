import asyncio
import nest_asyncio
import logging
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.functions import create_table

nest_asyncio.apply()

# Enable logging so you don't miss important messages
logging.basicConfig(level=logging.INFO)

API_TOKEN = 'YOUR_API'

# Bot object
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Start the process of polling new updates
async def main():
    dp.include_router(router)
 # Start creating the database table
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disabled')
