from routers.init import *

cmd_router = Router()

@cmd_router.message(CommandStart())
async def start(msg : Message):
  welcome_msg = get_welcome(user_id=str(msg.from_user.id), users=users)
  await msg.answer(text=welcome_msg, reply_markup=available_cmd(str(msg.from_user.id)))

@cmd_router.message(Command('flip'))
async def flip(msg : Message):
  coin = (FSInputFile('static/orel.webp'), FSInputFile('static/reshka.webp'))
  await bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.CHOOSE_STICKER)
  await bot.send_sticker(chat_id=msg.chat.id, sticker=coin[randint(0, 1)])

@cmd_router.message(Command('exit'))
async def exit(msg : Message):
  if users.permission(user_id=str(msg.from_user.id), perm='admin'):
    users.exit(user_id=str(msg.from_user.id))
    await clear_history(msg=msg, send_help=True)
    await msg.answer('Пользователь забыт')
  else: await msg.answer('Отказано в доступе')

@cmd_router.message(F.text.lower().startswith('/gen'))
async def gen_pass(msg : Message):
  ps = password.gen_password(key=msg.text[3::].replace(' ', ''))
  await msg.answer(text=f'`{ps}`', parse_mode='Markdown')

@cmd_router.message(Command('help'))
async def help(msg : Message):
  cmd = available_cmd(str(msg.from_user.id))
  await msg.answer(get_welcome(user_id=str(msg.from_user.id), users=users), reply_markup=cmd) 

@cmd_router.message(Command('allpass'))
async def allpass(msg : Message):
  if users.permission(user_id=str(msg.from_user.id), perm='admin'):
    ps = password.send_allpas()
    bot_msg = await msg.answer(text=ps, parse_mode='Markdown')
    await del_msg(bot_msg=bot_msg, user_msg=msg, delay=30)
  else: await msg.answer('Отказано в доступе')

@cmd_router.message(Command('files'))
async def send_files(msg : Message):
  if users.permission(user_id=str(msg.from_user.id), perm='admin'):
    bot_msgs = []
    path_files = all_files_path()
    for i in path_files:
      await bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
      file_name = i[len(FILE_PATH)+1::]
      send_files = await msg.answer_document(document=FSInputFile(i), caption=f'`{file_name}`', parse_mode='Markdown')
      bot_msgs += [send_files.message_id]

    await asyncio.sleep(90)
    for i in bot_msgs:
      await bot.delete_message(chat_id=msg.chat.id, message_id=i)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)

  else: await msg.answer('Отказано в доступе')

@cmd_router.message(Command('todolist'))
async def todolist(msg : Message):
  todolist_kb = get_todolist(user_id=str(msg.from_user.id), users=users)
  bot_msg = await msg.answer(text='Список дел', reply_markup=todolist_kb)
  await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)

@cmd_router.message(Command('chatgpt'))
async def chatgpt(msg : Message):
  text = f'{msg.from_user.id} {msg.from_user.username} хочет получить права на chatgpt'
  await bot.send_message(chat_id=OWN_CHAT_ID, text=text, reply_markup=chatgpt_kb)