from routers.init import *

cb_router = Router()

@cb_router.callback_query(F.data == 'clear_done')
async def clear_done(cb : CallbackQuery):
  await cb.answer('')
  user_id = str(cb.from_user.id)
  todolist.clear_done_task(column='task', user_id=str(cb.from_user.id))
  await cb.message.edit_reply_markup(reply_markup=get_todolist(user_id=user_id, todolist=todolist))

@cb_router.callback_query(F.data == 'add_new_task')
async def add_new_task_first(cb : CallbackQuery, state : FSMContext):
  await state.set_state(Add_new_task.new_task)
  await cb.answer('')
  await cb.message.answer('Введите новую задачу')

@cb_router.callback_query(F.data == 'note_task')
async def note_task(cb : CallbackQuery):
  await cb.answer('')
  user_id, username = str(cb.from_user.id), cb.from_user.username
  chat_id, msg_id = str(cb.message.chat.id), str(cb.message.message_id)

  todolist.add_values(column=('user_id', 'username'), no_copy=True, values=(user_id, username), id=user_id)
  
  note = users.get_value(column='note', user_id=str(cb.from_user.id))
  await bot.edit_message_text(text=note, chat_id=chat_id, message_id=msg_id, reply_markup=note_kb)

@cb_router.callback_query(F.data == 'back_task')
async def back_task(cb : CallbackQuery):
  await cb.answer('')
  todolist_kb = get_todolist(user_id=str(cb.from_user.id), todolist=todolist)
  msg_id, ct_id, txt = cb.message.message_id, cb.message.chat.id, 'Список дел'
  await bot.edit_message_text(text=txt, message_id=msg_id, chat_id=ct_id, reply_markup=todolist_kb)

@cb_router.callback_query(F.data == 'edit_note')
async def edit_note_first(cb : CallbackQuery, state : FSMContext):
  await state.set_state(Edit_note.note)
  await cb.answer('')
  note = users.get_value(column='note', user_id=str(cb.from_user.id))
  await cb.message.answer(text=f'`{note}`', parse_mode='Markdown')

@cb_router.callback_query(F.data == 'yes_gpt')
async def add_user_gpt(cb : CallbackQuery):
  user_id, username = cb.message.text.split()[0], cb.message.text.split()[1]
  users.add_values(no_copy=True, id=user_id, column=('user_id', 'username'), values=(user_id, username))
  users.update_value(column='gpt', value=1, id=user_id)
  await bot.delete_message(chat_id=cb.message.chat.id, message_id=cb.message.message_id)

@cb_router.callback_query(F.data == 'no_gpt')
async def no_gpt(cb : CallbackQuery):
  await bot.delete_message(chat_id=cb.message.chat.id, message_id=cb.message.message_id)

@cb_router.callback_query(F.data == 'yes_admin')
async def yes_login_admin(cb : CallbackQuery):
  user_id, username = cb.message.text.split()[0], cb.message.text.split()[1]
  users.add_values(no_copy=True, id=user_id, column=('user_id', 'username'), values=(user_id, username))
  users.update_value(column='admin', value=1, id=user_id)
  await bot.delete_message(chat_id=cb.message.chat.id, message_id=cb.message.message_id)

@cb_router.callback_query(F.data == 'no_admin')
async def no_login_admin(cb : CallbackQuery):
  await bot.delete_message(chat_id=cb.message.chat.id, message_id=cb.message.message_id)

@cb_router.callback_query(lambda c: c.data)
async def task_handler(cb : CallbackQuery):
  await cb.answer(text='')
  todolist.done_task(column='task', user_id=str(cb.from_user.id), task=cb.data)
  await cb.message.edit_reply_markup(reply_markup=get_todolist(user_id=str(cb.from_user.id), todolist=todolist))