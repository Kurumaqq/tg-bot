from aiogram.fsm.state import State, StatesGroup

class Add_new_task(StatesGroup):
  new_task = State()

class Edit_note(StatesGroup):
  note = State()