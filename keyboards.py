from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil
from database import Users, Todolist

admin_login_kb = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Да', callback_data='yes_admin'),
   InlineKeyboardButton(text='Нет', callback_data='no_admin')]
])

note_kb = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Назад', callback_data='back_task'), 
  InlineKeyboardButton(text='Изменить заметку', callback_data='edit_note')]
])

chatgpt_kb = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Yes', callback_data='yes_gpt'),
  InlineKeyboardButton(text='No', callback_data='no_gpt')]
])

def get_todolist(user_id : str, todolist : Todolist) -> InlineKeyboardMarkup:
  result = []
  task_list = todolist.get_values('task', user_id)
  for i in task_list:
    if i == None: continue
    result.append([InlineKeyboardButton(text=i, callback_data=i)])

  result.append([InlineKeyboardButton(text='Очистить 🗑️', callback_data='clear_done'),
                 InlineKeyboardButton(text='Добавить ➕', callback_data='add_new_task')])
  result.append([InlineKeyboardButton(text='Заметки 📒', callback_data='note_task')])
  return InlineKeyboardMarkup(inline_keyboard=result)
   
def get_available_cmd(user_id : str, users : Users, commands_list : list, commands : dict, row_len=3) -> ReplyKeyboardMarkup:
  keyboard_cmd = []
  iter_cmd = iter(commands_list)
  current_cmd = next(iter_cmd)
  len_keyboard = ceil(len(commands_list)/row_len)

  for i in range(len_keyboard):
      row = []
      for y in range(row_len):
          try:
            if users.check_perm(user_id, commands[current_cmd]['perm']):
              row.append(KeyboardButton(text=current_cmd))
              current_cmd = next(iter_cmd)
          except StopIteration:
            break

      keyboard_cmd.append(row)
  return ReplyKeyboardMarkup(keyboard=keyboard_cmd, resize_keyboard=True)