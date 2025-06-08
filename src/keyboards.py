from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from src.database import Users
from src.config import Config

config = Config()
users_db = Users()

admin_login_kb = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Да', callback_data='yes_admin'),
   InlineKeyboardButton(text='Нет', callback_data='no_admin')]
])

note_kb = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Назад', callback_data='back_task'), 
  InlineKeyboardButton(text='Изменить заметку', callback_data='edit_note')]
])

def commands_kb(user_id: str, columns: int = 3) -> ReplyKeyboardMarkup:
    result = []
    commands_dict = config.commands
    command_names = list(commands_dict.keys())
    
    for i in range(0, len(command_names), columns):
        row_buttons = []
        
        for cmd_name in command_names[i:i+columns]:
            cmd_data = commands_dict[cmd_name]
            
            if users_db.check_perm(user_id, cmd_data['perm']) and cmd_name[0] == '/':
                row_buttons.append(KeyboardButton(text=cmd_name))
        
        if row_buttons:
            result.append(row_buttons)

    return ReplyKeyboardMarkup(keyboard=result, resize_keyboard=True)
