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
  InlineKeyboardButton(text='No', callback_data='no_gpt')]])

def get_todolist(user_id : str, todolist : Todolist) -> InlineKeyboardMarkup:
  result = []
  task_list = todolist.get_values('task', user_id)
  for i in task_list:
    if i == None: continue
    print(i)
    result.append([InlineKeyboardButton(text=i, callback_data=i)])

  result.append([InlineKeyboardButton(text='Очистить 🗑️', callback_data='clear_done'),
                 InlineKeyboardButton(text='Добавить ➕', callback_data='add_new_task')])
  result.append([InlineKeyboardButton(text='Заметки 📒', callback_data='note_task')])
  return InlineKeyboardMarkup(inline_keyboard=result)
   

def get_available_cmd(user_id : str, users : Users, commands_list : list, commands : dict, row_line=3) -> ReplyKeyboardMarkup:
  keyboard_cmd = []
  i_cmd = iter(commands_list)
  current_cmd = next(i_cmd)
  len_keyboard = ceil(len(commands_list)/row_line)

  for _ in range(len_keyboard):
      row_line = []
      for _ in range(3):
          try:
            if users.check_perm(user_id, commands[current_cmd]['perm']):
              row_line.append(KeyboardButton(text=current_cmd))
              current_cmd = next(i_cmd)
          except StopIteration:
            break

      keyboard_cmd.append(row_line)


  return ReplyKeyboardMarkup(keyboard=keyboard_cmd, resize_keyboard=True)