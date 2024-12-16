from routers.init import bot
from datetime import datetime, timedelta
from cfg import DATABASE_PATH, OWN_CHAT_ID, get_pay_date
import asyncio

async def pay_me(msg : str) -> None:
  pay_date = get_pay_date()
  while True:
    await asyncio.sleep(21_600)
    date_now = datetime.now().strftime('%d.%m.%y')
    if date_now == pay_date:
      with open(f'{DATABASE_PATH}/pay_date.txt', 'w') as file:
        next_pay_date = (datetime.now() + timedelta(days=25)).strftime('%d.%m.%y')
        file.write(next_pay_date)
      await bot.send_message(chat_id=OWN_CHAT_ID, text=msg)
      pay_date = get_pay_date()