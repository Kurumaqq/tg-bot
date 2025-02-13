from routers.imports import *

fsm_router = Router()

@fsm_router.message(Add_new_task.new_task)
async def add_new_task_second(msg : Message, state : FSMContext):
  if len(msg.text) < 30:
    await state.clear()
    user = User_properties(msg)
    task = msg.text
    
    todolist_db.add_values(column=('user_id', 'username', 'task'), values=(user.id, user.name, task))
    todolist_kb = get_todolist(user_id=user.id, todolist=todolist_db)
    await clear_history(msg=msg, limit=4, send_help=False)
    bot_msg = await msg.answer(text='Список дел', reply_markup=todolist_kb)
    await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)
  else:
    await msg.answer('Слишком много символов, задача не должна превышать 30 символ!!!')


@fsm_router.message(Edit_note.note)
async def edit_note_second(msg : Message, state : FSMContext):
  user = User_properties(msg)
  new_note = msg.text

  users_db.add_values(no_copy=True, column=('user_id', 'username'), values=(user.id, user.name), id=user.id)
  users_db.update_value(column='note', value=new_note, id=user.id)
  note = users_db.get_value(column='note', user_id=user.id)

  await clear_history(msg=msg, limit=3, send_help=False)
  bot_msg = await msg.answer(text=note, reply_markup=note_kb)
  await state.clear()
  await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)
