from routers.init import *

cmd_text_router = Router()

@cmd_text_router.message(F.text == PASSWORD)
async def add_admin(msg : Message):
  users.add_admin(user_id=str(msg.from_user.id), username=msg.from_user.username)
  await msg.answer('Права администратора получены')
  welcome_msg = get_welcome(user_id=str(msg.from_user.id), users=users)
  await msg.answer(text=welcome_msg, reply_markup=available_cmd(str(msg.from_user.id)))
  await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)

@cmd_text_router.message(F.text.lower().startswith('/gen'))
async def gen_pass(msg : Message):
  ps = password.gen_password(key=msg.text[3::].replace(' ', ''))
  await msg.answer(text=f'`{ps}`', parse_mode='Markdown')

@cmd_text_router.message(F.text.lower().startswith('p- '))
async def del_pass(msg : Message):
  if users.permission(user_id=str(msg.from_user.id), perm='admin'):
    app = msg.text[3::].strip()
    password.del_password(app=app)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
  else: await msg.answer('Отказано в доступе')

@cmd_text_router.message(F.text.lower().startswith('p+ '))
async def add_pass(msg : Message):
  if users.permission(user_id=str(msg.from_user.id), perm='admin'):
    if len(msg.text[3::].split()) >= 2:
      app, ps = msg.text[3::].split()
      password.add_password(app=app, password=ps)
    else: msg.answer('Ошибка!!')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
  else: await msg.answer('Отказано в доступе')

@cmd_text_router.message(F.text.lower().startswith('p '))
async def pass_from_key(msg : Message):
  if users.permission(user_id=str(msg.from_user.id), perm='admin'):
    key = msg.text[2::]
    ps = password.password_from_key(key=key)
    bot_msg = await msg.reply(text=f'`{ps}`', parse_mode='Markdown')
    await del_msg(bot_msg=bot_msg, user_msg=msg, delay=7)
  else: await msg.answer('Отказано в доступе')

@cmd_text_router.message(F.text.lower().startswith('f- '))
async def del_files(msg : Message):
  try:
    os.remove(f'{FILE_PATH}/{msg.text[3::]}')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
  except:  
    await msg.answer('Ошибка!!!')

@cmd_text_router.message(F.content_type == ContentType.TEXT)
async def gpt(msg : Message):
  if users.permission(user_id=str(msg.from_user.id), perm='gpt'):
    msg_edited = await msg.answer('Генерация ответа...')
    msg_edited_id = msg_edited.message_id
    chat_id = msg_edited.chat.id
    await bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)

    try:
      response = await ask_gpt(msg.text)
      await bot.edit_message_text(text=response, chat_id=chat_id, 
                                  message_id=msg_edited_id, parse_mode='Markdown')
    except:
      await bot.edit_message_text(text=response, chat_id=chat_id, message_id=msg_edited_id)