from routers.imports import *

cmd_text_router = Router()

@cmd_text_router.message(F.text == PASSWORD)
async def add_admin(msg : Message):
  user = User_properties(msg)
  if add_ignored_user(user.id, users_db, 'admin'):
    txt = f'{user.id} {user.name} хочет получить права администратора'
    await bot.send_message(chat_id=OWN_CHAT_ID, text=txt, reply_markup=admin_login_kb)
    await bot.delete_message(chat_id=user.id, message_id=user.msg_id)

@cmd_text_router.message(F.text.lower().startswith('p- '))
async def del_pass(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user.id, 'admin'):
    app = msg.text[3::].strip()
    password_db.del_value(user_id=app, column='app')
    await bot.delete_message(chat_id=user.chat_id, message_id=user.msg_id)

@cmd_text_router.message(F.text.lower().startswith('p+ '))
async def add_pass(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user.id, 'admin'):
    if len(msg.text[3::].split()) >= 2:
      app, ps = msg.text[3::].split()
      password_db.add_values(column=('app', 'password'), values=(app, ps), 
                          no_copy=True, id=app, condition='app')
      
    else: msg.answer('Ошибка!!')
    await bot.delete_message(chat_id=user.chat_id, message_id=user.msg_id)

@cmd_text_router.message(F.text.lower().startswith('p '))
async def pass_from_key(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user.id, 'admin'):
    key = msg.text[2::]
    ps = password_db.get_value(column='password', user_id=key, condition='app')
    bot_msg = await msg.reply(text=f'`{ps}`', parse_mode='Markdown')
    await del_msg(bot_msg=bot_msg, user_msg=msg, delay=7)

@cmd_text_router.message(F.text.lower().startswith('f- '))
async def del_files(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user.id, 'admin'):
    try:
      os.remove(f'{FILE_PATH}/{msg.text[3::]}')
      await bot.delete_message(chat_id=user.chat_id, message_id=user.msg_id)
    except: await msg.answer('Ошибка!!!')

@cmd_text_router.message(F.content_type == ContentType.TEXT)
async def gpt(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user_id=user.id, perm='gpt'):
    msg_edited = await msg.answer('Генерация ответа...')
    msg_id = msg_edited.message_id
    txt = await ask_gpt(msg.text)
    await bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)

    try:
      await bot.edit_message_text(text=txt, chat_id=user.chat_id, message_id=msg_id, parse_mode='Markdown')
    except:
      await bot.edit_message_text(text=txt, chat_id=user.chat_id, message_id=msg_id)