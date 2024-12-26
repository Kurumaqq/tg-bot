from dotenv import load_dotenv
from os import getenv

load_dotenv()
DATABASE_PATH = 'database'
FILE_PATH = 'files'
TOKEN = getenv('TOKEN')
PASSWORD = getenv('PASSWORD')
OWN_CHAT_ID = getenv('OWN_CHAT_ID')
CMD = {
      '/help': {'desc': 'все команды', 'perm': None},
      '/flip': {'desc': 'подкинуть монетку', 'perm': None}, 
      '/gen': {'desc': 'сгенерировать пароль', 'perm': None},
      '/todolist': {'desc': 'открыть список дел', 'perm': None},
      '/files': {'desc': 'отправить все файлы', 'perm': 'admin'},
      '/exit': {'desc': 'забыть пользователя', 'perm': 'admin'},
      '/allpass': {'desc': 'отправить все пароли', 'perm': 'admin'},
      '[photo]': {'desc': 'убрать фон у картинки', 'perm': None},
      'f- [name]': {'desc': 'удалить файл', 'perm': 'admin'},
      'p [app]': {'desc': 'пароль от приложения', 'perm': 'admin'},
      'p- [app]': {'desc': 'удалить пароль', 'perm': 'admin'},
      'p+ [app] [password]': {'desc': 'добавить пароль', 'perm': 'admin'},
      }
CMD_KB = [i for i in CMD if i[0] == '/']

ignored_gpt = {'gpt' : [], 'admin' : []}

def add_ignored_user(user_id : str, users, cmd : str):
  if user_id in ignored_gpt[cmd] or users.check_perm(user_id, perm=cmd): return False

  ignored_gpt[cmd].append(user_id)
  return True

def get_pay_date():
  with open(f'{DATABASE_PATH}/pay_date.txt', 'r') as file:
    return file.read()

def get_help(user_id : str, users) -> str:
  result = 'Добро пожаловать!!! \n\n'

  for i in CMD:
    if users.check_perm(user_id, CMD[i]['perm']):
      result += f'{i}  -  {CMD[i]["desc"]} \n\n'

  return result