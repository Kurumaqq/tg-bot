from routers.init import *

fsm_router = Router()

@fsm_router.message(Add_new_task.new_task)
async def add_new_task_second(msg : Message, state : FSMContext):
  if len(msg.text) < 30:
    users.add_task(user_id=str(msg.from_user.id), username=msg.from_user.username, task=msg.text)
    await clear_history(msg=msg, limit=4, send_help=False)
    todolist_kb = get_todolist(user_id=str(msg.from_user.id), users=users)
    bot_msg = await msg.answer(text='Список дел', reply_markup=todolist_kb)
    await state.clear()
    await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)
  else:
    await state.clear()
    await msg.answer('Слишком много символов, задача не должна превышать 31 символ!!!')


@fsm_router.message(Edit_note.note)
async def edit_note_second(msg : Message, state : FSMContext):
  users.update_note(user_id=str(msg.from_user.id), note=msg.text)
  note = users.get_note(user_id=str(msg.from_user.id))
  await clear_history(msg=msg, limit=3, send_help=False)
  bot_msg = await msg.answer(text=note, reply_markup=note_kb)
  await state.clear()
  await del_msg(bot_msg=bot_msg, user_msg=msg, delay=300)
