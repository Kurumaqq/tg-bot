import asyncio
from aiogram import Bot, Dispatcher
from src.routers.router_master import router_master 
from src.config import Config

config = Config()
bot = Bot(config.token)
dp = Dispatcher()

async def main():   
  dp.include_routers(*router_master)
  await dp.start_polling(bot)

if __name__ == '__main__':
  asyncio.run(main())
