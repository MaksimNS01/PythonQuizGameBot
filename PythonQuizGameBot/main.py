import asyncio
import nest_asyncio
import logging
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.functions import create_table

nest_asyncio.apply()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = '7832350438:AAEl8j5_aR0FAJEQTS6dOodwifmc8vfgyLs'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(router)
    # Запускаем создание таблицы базы данных
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот отключён')