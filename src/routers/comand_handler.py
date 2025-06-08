from aiogram.filters import CommandStart, Command
from aiogram.enums.chat_action import ChatAction
from aiogram.types import Message, FSInputFile
from aiogram import Router, Bot, F
from src.database import Users, Password
from src.utils import get_help_text, del_msg
from src.utils import User_properties
from src.keyboards import commands_kb
from random import randint

cmd_router = Router()
users_db = Users()
password_db = Password()

@cmd_router.message(CommandStart())
async def start(msg : Message):
    user = User_properties(msg)
    welcome_msg = get_help_text(user_id=user.id, users=users_db)
    await msg.answer(text=welcome_msg, reply_markup=commands_kb(user.id))

@cmd_router.message(Command('flip'))
async def flip(msg : Message, bot: Bot):
    user = User_properties(msg)
    coin = (FSInputFile('assets/orel.webp'), FSInputFile('assets/reshka.webp'))
    await bot.send_chat_action(chat_id=user.chat_id, action=ChatAction.CHOOSE_STICKER)
    await bot.send_sticker(chat_id=user.chat_id, sticker=coin[randint(0, 1)])

@cmd_router.message(Command('exit'))
async def exit(msg : Message):
    user = User_properties(msg)
    if users_db.check_perm(user.id, 'admin'):
        users_db.update_value(column='admin', value=0, id=user.id)
        await msg.answer('Пользователь забыт')

@cmd_router.message(F.text.lower().startswith('/gen'))
async def gen_pass(msg : Message):
    ps = password_db.generation(key=msg.text[3::].replace(' ', ''))
    await msg.answer(text=f'`{ps}`', parse_mode='Markdown')

@cmd_router.message(Command('help'))
async def help(msg : Message):
    user = User_properties(msg)
    help_text = get_help_text(user.id, users_db)
    await msg.answer(text=help_text, reply_markup=commands_kb(user.id_int)) 

@cmd_router.message(Command('allpass'))
async def allpass(msg : Message, bot: Bot):
    user = User_properties(msg)
    if users_db.check_perm(user.id, 'admin'):
        passwords = password_db.get_passwords()
        bot_msg = await msg.answer(text=passwords, parse_mode='Markdown')
        await del_msg(bot_msg=bot_msg, user_msg=msg, bot=bot, delay=30)
