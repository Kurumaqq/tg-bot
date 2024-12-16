import sqlite3 as sq
from random import randint
from cfg import DATABASE_PATH


class Password():
  SYMBOLS = '!$&/'
  LETTERS = 'qwertyuiopasdfghjklzxcvbnm'
  NUMBERS = '1234567890'
  ALL_CHARACTERS = SYMBOLS + LETTERS + NUMBERS

  # Генерируем список всех паролей из базы данных
  @property
  def passwords(self) -> list:
    with sq.connect(f'{DATABASE_PATH}/passwords.db') as con:
      cur = con.cursor()
      return cur.execute('''SELECT * FROM passwords''').fetchall()

  @passwords.setter 
  def passwords(self) -> None:
    pass
  
  # Удалить пароль из базы данных
  def del_password(self, app : str) -> None:
    with sq.connect(f'{DATABASE_PATH}/passwords.db') as con:
      cur = con.cursor()
      passwords_list = [i[0] for i in self.passwords]
      if app in passwords_list:
        cur.execute('DELETE FROM passwords WHERE app = ?', (app,))

  # Добавление пролей в базу данных
  def add_password(self, app : str, password : str) -> str:
    with sq.connect(f'{DATABASE_PATH}/passwords.db') as con:
      cur = con.cursor()
      passwords = [i[0] for i in self.passwords]

      if app not in passwords:
        cur.execute('INSERT INTO passwords (app, password) VALUES (?, ?)', (app, password))

  # Получение пароля по ключу
  def password_from_key(self, key : str) -> str:
    with sq.connect(f'{DATABASE_PATH}/passwords.db') as con:
      cur = con.cursor()
      result = cur.execute(f'SELECT password FROM passwords WHERE app = ?', (key,)).fetchone()
      return result[0] if result != None else 'No password'

  # Генерация пароля
  def gen_password(self, key : str, length=15) -> str:
    password = ''

    if length - len(key) > 5:  password_len = length - len(key)
    else:  password_len = length + round(len(key) /2)

    for i in range(password_len):
      if i == round(password_len / 2): 
        for i in key:
          password += self.random_translit(i)

      else: password +=  self.random_translit(self.ALL_CHARACTERS[randint(0, (len(self.ALL_CHARACTERS) - 1))])
    password = password.replace(password[0], self.random_translit(self.LETTERS[randint(0, len(self.LETTERS) - 1)])) 
    return password
  
  # Отправка всех парлей из базы данных
  def send_allpas(self) -> str:
    text  = ''
    for i in self.passwords:
      text += f"{i[0]}  -  `{i[1]}`\n\n"

    return text
  
  # Случайный пароль
  def random_translit(self, text : str) -> str:
    rnd = randint(0, 1)
    return text.lower() if rnd == 1 else text.upper()