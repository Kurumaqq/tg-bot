from routers.init import *

fsm_router = Router()

@fsm_router.message(Add_new_task.new_task)
async def add_new_task_second(msg : Message, state : FSMContext):
  if len(msg.text) < 30:
    user_id = str(msg.from_user.id)
    username = msg.from_user.username
    task = msg.text
    todolist_kb = get_todolist(user_id=str(msg.from_user.id), todolist=todolist)
    
    todolist.add_values(column=('user_id', 'username', 'task'), values=(user_id, username, task))
    await clear_history(msg=msg, limit=4, send_help=False)
    bot_msg = await msg.answer(text='Список дел', reply_markup=todolist_kb)
    await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)
  else:
    await msg.answer('Слишком много символов, задача не должна превышать 31 символ!!!')

  await state.clear()
  # test

@fsm_router.message(Edit_note.note)
async def edit_note_second(msg : Message, state : FSMContext):
  new_note = msg.text
  user_id = str(msg.from_user.id)
  username = msg.from_user.username
  note = users.get_value(column='note', user_id=user_id)

  users.add_values(no_copy=True, column=('user_id', 'username'), values=(user_id, username))
  users.update_value(column='note', value=new_note, id=user_id)

  await clear_history(msg=msg, limit=3, send_help=False)
  bot_msg = await msg.answer(text=note, reply_markup=note_kb)
  await state.clear()
  await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)
