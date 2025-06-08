from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from src.keyboards import commands_kb
from src.database import Users
from src.config import Config
import asyncio

config = Config()
users_db = Users()

class User_properties():
    def __init__(self, user : Message | CallbackQuery):
        self.name = user.from_user.username
        self.id = str(user.from_user.id)
        self.id_int = user.from_user.id

        if isinstance(user, Message):
            self.msg_id = user.message_id
            self.chat_id = user.chat.id
          
        elif isinstance(user, CallbackQuery):
            self.msg_id = user.message.message_id
            self.chat_id = user.message.chat.id
        else: raise TypeError
            
async def del_msg(bot_msg: Message, user_msg: Message, bot: Bot, delay=0):
  await asyncio.sleep(delay)
  try:
    await bot.delete_message(chat_id=bot_msg.chat.id, message_id=bot_msg.message_id)
    await bot.delete_message(chat_id=user_msg.chat.id, message_id=user_msg.message_id)
  except: return

async def clear_history(msg: Message, bot: Bot, limit=0, send_help=True) -> None:
    limit = msg.message_id-limit if limit > 0 else limit
    user_id = str(msg.from_user.id)
    try:
      for i in range(msg.message_id, limit, -1):
        await bot.delete_message(msg.from_user.id, i)
    except TelegramBadRequest as ex:
        if send_help:
          await msg.answer(
             get_help_text(user_id=user_id, users=users_db), 
             reply_markup=commands_kb(user_id)
             )

def commands_kb(user_id : str):
  return commands_kb(
     user_id=user_id, 
    users_db=users_db, 
    commands_list=commands_kb, 
    commands=config.commands
    )

def get_help_text(user_id : str, users) -> str:
    text = 'Добро пожаловать!!! \n\n'
    commands = config.commands

    for i in commands:
        if users.check_perm(user_id, commands[i]['perm']):
            text += f'{i}  -  {commands[i]["desc"]} \n\n'

    return text
