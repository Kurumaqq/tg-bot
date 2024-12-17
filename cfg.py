DATABASE_PATH = 'database'
FILE_PATH = 'files'
# TOKEN = '7770405490:AAEYctkKfuq4K2AgVnP2ojND-EOgJ3aoQUM'
TOKEN = '6633787639:AAG6rIVWzdy1rZK4AT3jZUDWuE6u1-ablQA' # Test bot token
PASSWORD = 'k1682qq'
OWN_CHAT_ID = '1044605359'
CMD = {
      '/help': {'desc': 'все команды', 'perm': None},
      '/flip': {'desc': 'подкинуть монетку', 'perm': None}, 
      '/gen': {'desc': 'сгенерировать пароль', 'perm': None},
      '/todolist': {'desc': 'открыть список дел', 'perm': None},
      '/files': {'desc': 'отправить все файлы', 'perm': 'admin'},
      '/exit': {'desc': 'забыть пользователя', 'perm': 'admin'},
      '/allpass': {'desc': 'отправить все пароли', 'perm': 'admin'},
      'f- [name]': {'desc': 'удалить файл', 'perm': 'admin'},
      'p [app]': {'desc': 'пароль от приложения', 'perm': 'admin'},
      'p- [app]': {'desc': 'удалить пароль', 'perm': 'admin'},
      'p+ [app] [password]': {'desc': 'добавить пароль', 'perm': 'admin'},
      }
CMD_KB = [i for i in CMD if i[0] == '/']

ignored_users = []

def add_ignored_user(user_id : str, users):
  if user_id not in ignored_users or users.perm(user_id, perm='gpt'):
    ignored_users.append(user_id)
    return False
  return True

def get_pay_date():
  with open(f'{DATABASE_PATH}/pay_date.txt', 'r') as file:
    return file.read()

def get_welcome(user_id : str, users) -> str:
  result = 'Добро пожаловать!!! \n\n'

  for i in CMD:
    if i == '/gpt':continue
    if users.perm(user_id=user_id, perm=CMD[i]['perm']):
      result += f'{i}  -  {CMD[i]["desc"]} \n\n'

  return result