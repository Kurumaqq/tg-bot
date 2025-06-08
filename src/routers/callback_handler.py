from aiogram.types import CallbackQuery
from aiogram import Bot, F, Router
from src.utils import User_properties
from src.database import Users

cb_router = Router()
users_db = Users()

@cb_router.callback_query(F.data == 'yes_admin')
async def yes_login_admin(cb : CallbackQuery, bot: Bot):
    user = User_properties(cb)
    user_id, username = cb.message.text.split()[0], cb.message.text.split()[1]
    users_db.add_values(
        no_copy=True, id=user_id, 
        column=('user_id', 'username'), 
        values=(user_id, username)
        )
    users_db.update_value(column='admin', value=1, id=user_id)
    await bot.delete_message(chat_id=user.chat_id, message_id=user.msg_id)

@cb_router.callback_query(F.data == 'no_admin')
async def no_login_admin(cb : CallbackQuery, bot: Bot):
    await bot.delete_message(
        chat_id=cb.message.chat.id, 
        message_id=cb.message.message_id
        )
