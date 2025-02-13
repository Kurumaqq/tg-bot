from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile, InputFile
from aiogram.filters import Command, CommandStart
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from cfg import (get_help, TOKEN, CMD, CMD_KB, PASSWORD, 
                 FILE_PATH, OWN_CHAT_ID, add_ignored_user,
                 DATABASE_PATH)
from keyboards import get_available_cmd, get_todolist, note_kb, chatgpt_kb, admin_login_kb
from fsm import *
from user_properties import User_properties
from database import Users, Password, Todolist
from chatgpt import ask_gpt
import asyncio
from files import get_file_path
import os
from random import randint

from rembg import remove
from PIL import Image

bot = Bot(token=TOKEN)
dp = Dispatcher()
users_db = Users()
todolist_db = Todolist()
password_db = Password()

async def del_msg(bot_msg : Message, user_msg : Message, delay=0):
  await asyncio.sleep(delay)
  try:
    await bot.delete_message(chat_id=bot_msg.chat.id, message_id=bot_msg.message_id)
    await bot.delete_message(chat_id=user_msg.chat.id, message_id=user_msg.message_id)
  except:
    pass

async def clear_history(msg: Message, limit=0, send_help=True) -> None:
    limit = msg.message_id-limit if limit > 0 else limit
    user_id = str(msg.from_user.id)
    try:
      for i in range(msg.message_id, limit, -1):
        await bot.delete_message(msg.from_user.id, i)
    except TelegramBadRequest as ex:
      if ex.message == "Bad Request: message to delete not found":
        if send_help:
          await msg.answer(get_help(user_id=msg.from_user.id, users=users_db), reply_markup=available_cmd(user_id))

def available_cmd(user_id : str):
  return get_available_cmd(user_id=user_id, users=users_db, commands_list=CMD_KB, commands=CMD)

