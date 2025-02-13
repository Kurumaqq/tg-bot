from routers.imports import *

cmd_router = Router()

@cmd_router.message(CommandStart())
async def start(msg : Message):
  user = User_properties(msg)
  welcome_msg = get_help(user_id=user.id, users=users_db)
  await msg.answer(text=welcome_msg, reply_markup=available_cmd(user.id))

@cmd_router.message(Command('flip'))
async def flip(msg : Message):
  user = User_properties(msg)
  coin = (FSInputFile('static/orel.webp'), FSInputFile('static/reshka.webp'))
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
  cmd = available_cmd(user.id)
  help_text = get_help(user.id, users_db)
  await msg.answer(text=help_text, reply_markup=cmd) 

@cmd_router.message(Command('allpass'))
async def allpass(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user.id, 'admin'):
    passwords = password_db.send_passwords()
    bot_msg = await msg.answer(text=passwords, parse_mode='Markdown')
    await del_msg(bot_msg=bot_msg, user_msg=msg, delay=30)

@cmd_router.message(Command('files'))
async def send_files(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user.id, 'admin'):
    bot_msgs = []
    path_files = get_file_path()
    for i in path_files:
      await bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
      file_name = i[len(FILE_PATH)+1::]
      send_files = await msg.answer_document(document=FSInputFile(i), caption=f'`{file_name}`', parse_mode='Markdown')
      bot_msgs += [send_files.message_id]

    await asyncio.sleep(90)
    for i in bot_msgs: await bot.delete_message(chat_id=user.chat_id, message_id=i)
    await bot.delete_message(chat_id=user.chat_id, message_id=user.msg_id)

@cmd_router.message(Command('todolist'))
async def send_todolist(msg : Message):
  user = User_properties(msg)
  todolist_kb = get_todolist(user_id=user.id, todolist=todolist_db)
  bot_msg = await msg.answer(text='Список дел', reply_markup=todolist_kb)
  await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)

@cmd_router.message(Command('chatgpt'))
async def chatgpt(msg : Message):
  user = User_properties(msg)
  if add_ignored_user(user.id, users_db,'gpt'):
    text = f'{user.id} {user.name} хочет получить права на chatgpt'
    await bot.send_message(chat_id=OWN_CHAT_ID, text=text, reply_markup=chatgpt_kb)