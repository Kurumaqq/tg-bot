import sqlite3 as sq
from random import randint

class Database():
  def __init__(self):
    self.db_path = ''
    self.db_name = ''
    self.table = ''

  def get_values(self, column : tuple, user_id='', condition='user_id') -> tuple[tuple]:
    with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      col = self.get_column(column)
      if user_id != '': 
        sql_cmd = f'SELECT {col} FROM {self.table} WHERE {condition} = ?'
        if isinstance(column, str): 
          result = tuple(i[0] for i in cur.execute(sql_cmd, (user_id, )).fetchall())
        else: result = tuple(cur.execute(sql_cmd, (user_id, )).fetchall())

      else: 
        col = self.get_column(column) 
        sql_cmd = f'SELECT {col} FROM {self.table}'
        if isinstance(column, str): result = tuple(i[0] for i in cur.execute(sql_cmd).fetchall())
        else: result = tuple((i) for i in cur.execute(sql_cmd).fetchall())

      return result

  def get_value(self, column : str, user_id : str, convert_bool=False, condition='user_id'):
    with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      sql_cmd =  f'SELECT {column} FROM {self.table} WHERE {condition} = ?'
      result = cur.execute(sql_cmd, (user_id, )).fetchone()[0]
      try:
        if convert_bool and isinstance(result, int): result = bool(result)
      except: print('Невозможно преобразовать в bool!!!')
      return result


  def update_value(self, column : str, value : any, id : str) -> None:
    
    with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      cur.execute(f'UPDATE {self.table} SET {column} = ? WHERE  user_id = ?', 
                  (value, id,))

  def add_values(self, column : tuple, values : tuple, no_copy=False, id='', condition='user_id') -> str:
    tmp_values = '('
    col = '('
    if no_copy: id_list = self.get_values(column=condition)

    for i in range(len(column) - 1): tmp_values += '?, '
    else: tmp_values += '?)'

    for i in column: col += f'{i}, '
    else: col = col[:-2] + ')'
    if no_copy and id in id_list: return'Данные уже существуют!!'

    with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      cur.execute(f'INSERT INTO {self.table} {col} VALUES {tmp_values}', values)
    
    return 'Успешно!'

  def del_value(self, user_id : str, column : str) -> None:
    with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      cur.execute(f'DELETE FROM {self.table} WHERE {column} = ?', (user_id,))


  def get_column(self, column : tuple):
    col = ''
    if type(column) == tuple:
      for i in range(len(column)):
        if i == len(column) -1: col += column[i]
        else: col += f"{column[i]}, "
    else: col = column
    return col

class Users(Database):
  def __init__(self):
    self.db_path = 'database'
    self.db_name = 'users.db'
    self.table = 'users'

  def check_perm(self, user_id : str, perm : str):
    with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      sql_cmd = f'SELECT {perm} FROM users WHERE user_id = ?'
      if perm == None: return True
      try: return bool(cur.execute(sql_cmd, (user_id, )).fetchone()[0])
      except: return None

class Password(Database):
  SYMBOLS = '!$&/'
  LETTERS = 'qwertyuiopasdfghjklzxcvbnm'
  NUMBERS = '1234567890'
  ALL_CHARACTERS = SYMBOLS + LETTERS + NUMBERS
  def __init__(self):
    self.db_path = 'database'
    self.db_name = 'passwords.db'
    self.table = 'passwords'

  def generation(self, key, length=15):
    password = ''

    if length - len(key) > 5:  password_len = length - len(key)
    else:  password_len = length + round(len(key) /2)

    for i in range(password_len):
      if i == round(password_len / 2): 
        for i in key: password += self.random_register(i)
      else: password +=  self.random_register(self.ALL_CHARACTERS[randint(0, (len(self.ALL_CHARACTERS) - 1))])
    return password.replace(password[0], self.random_register(self.LETTERS[randint(0, len(self.LETTERS) - 1)])) 

  def send_passwords(self):
    password_list = self.get_values(('app', 'password'))
    all_password = ''
    for i in password_list: all_password += f'{i[0]} - `{i[1]}` \n\n'
    return all_password

  def random_register(self, text : str) -> str:
    rd = randint(0, 1)
    return text.lower() if rd == 1 else text.upper()

class Todolist(Database):
  def __init__(self):
    self.db_path = 'database'
    self.db_name = 'todolist.db'
    self.table = 'todolist'

  def done_task(self, column : str,  user_id : str, task : str) -> None:
     with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      if task[-1] == '☑':
        cur.execute(f'UPDATE {self.table} SET {column} = ? WHERE  {column} = ? AND user_id = ?', 
                    (f'{task[:-1:]}', task, user_id,))
      else: 
        cur.execute(f'UPDATE {self.table} SET {column} = ? WHERE {column} = ? AND user_id = ?', 
                    (f'{task}☑', task, user_id,))
        
  def clear_done_task(self, column : str, user_id : str) -> None:
    with sq.connect(f'{self.db_path}/{self.db_name}') as con:
      cur = con.cursor()
      cur.execute(f'DELETE FROM {self.table} WHERE {column} LIKE "%☑" AND user_id = ?', (user_id,))