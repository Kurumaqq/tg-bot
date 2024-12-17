from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile, InputFile
from aiogram.filters import Command, CommandStart
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from cfg import (get_welcome, TOKEN, CMD, CMD_KB, PASSWORD, 
                 FILE_PATH, OWN_CHAT_ID, add_ignored_user,
                 DATABASE_PATH)
from keyboards import get_available_cmd, get_todolist, note_kb, chatgpt_kb
from fsm import *
from users import Users
from password import Password
from chatgpt import ask_gpt
import asyncio
from files import all_files_path
import os
from random import randint

from rembg import remove
from PIL import Image

bot = Bot(token=TOKEN)
dp = Dispatcher()
users = Users(DATABASE_PATH)
password = Password() 

async def del_msg(bot_msg : Message, user_msg : Message, delay=0):
  await asyncio.sleep(delay)
  try:
    await bot.delete_message(chat_id=bot_msg.chat.id, message_id=bot_msg.message_id)
    await bot.delete_message(chat_id=user_msg.chat.id, message_id=user_msg.message_id)
  except:
    pass

async def clear_history(msg: Message, limit=0, send_help=True) -> None:
    limit = msg.message_id-limit if limit > 0 else limit
    try:
      for i in range(msg.message_id, limit, -1):
        await bot.delete_message(msg.from_user.id, i)
    except TelegramBadRequest as ex:
      if ex.message == "Bad Request: message to delete not found":
        if send_help:
          await msg.answer(get_welcome(user_id=msg.from_user.id, users=users), reply_markup=available_cmd(user_id=msg))

def available_cmd(user_id : str):
  return get_available_cmd(users_id=user_id, users=users, commands_list=CMD_KB, commands=CMD)

