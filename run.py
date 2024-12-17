from routers.init import bot, dp
from routers.all import router_master
import asyncio
from notify import pay_me

async def main():   
  dp.include_routers(*router_master)
  asyncio.create_task(pay_me('Оплати меня хуесос!!!'))
  await dp.start_polling(bot)

if __name__ == '__main__':
  asyncio.run(main())