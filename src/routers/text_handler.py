from aiogram import Router, Bot, F
from cryptography.fernet import Fernet
from aiogram.types import Message
from src.database import Users, Password
from src.keyboards import admin_login_kb
from src.utils import User_properties
from src.config import Config
from src.utils import del_msg

cmd_text_router = Router()
config = Config()
password_db = Password()
users_db = Users()
ignored_user = []
cipher = Fernet(config.encrypt_key)


@cmd_text_router.message(F.text == config.password)
async def add_admin(msg : Message, bot: Bot):
    user = User_properties(msg)
    if user.id in ignored_user: return
    ignored_user.append(user.id)

    txt = f'{user.id} {user.name} хочет получить права администратора'
    await bot.send_message(
    reply_markup=admin_login_kb,
    chat_id=config.own_chat_id, 
    text=txt
    )
    await bot.delete_message(chat_id=user.id, message_id=user.msg_id)

@cmd_text_router.message(F.text.lower().startswith('p- '))
async def del_pass(msg : Message, bot: Bot): 
    user = User_properties(msg)
    if users_db.check_perm(user.id, 'admin'):
        app = msg.text[3::].strip()
        password_db.del_value(user_id=app, column='app')
        await bot.delete_message(
            chat_id=user.chat_id, 
            message_id=user.msg_id
            )

@cmd_text_router.message(F.text.lower().startswith('p+ '))
async def add_pass(msg : Message, bot: Bot):
    user = User_properties(msg)
    if users_db.check_perm(user.id, 'admin'):
        if len(msg.text[3::].split()) >= 2:
            app, ps = msg.text[3::].split()
            encrytp_pass = cipher.encrypt(ps.encode())
            password_db.add_values(
                column=('app', 'password'), 
                values=(app, encrytp_pass), 
                condition='app',
                no_copy=True, 
                id=app, 
            )
    else: msg.answer('Ошибка!!')
    await bot.delete_message(chat_id=user.chat_id, message_id=user.msg_id)

@cmd_text_router.message(F.text.lower().startswith('p '))
async def pass_from_key(msg : Message, bot: Bot):
    user = User_properties(msg)
    if users_db.check_perm(user.id, 'admin'):
        key = msg.text[2::]
        try: 
            ps = password_db.get_value(column='password', user_id=key, condition='app')
            decrypt_ps = cipher.decrypt(ps).decode()
            bot_msg = await msg.reply(text=f'`{decrypt_ps}`', parse_mode='Markdown')

        except:
            bot_msg = await msg.answer(text='Такого пароля не существует!!!')
        
        await del_msg(bot_msg=bot_msg, bot=bot, user_msg=msg, delay=7)
