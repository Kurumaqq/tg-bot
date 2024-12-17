import sqlite3 as sq

class Users():
  def __init__(self, database_path : str):
    self.database_path = database_path

  @property
  def todolist(self) -> list[tuple]:
    with sq.connect(f'{self.database_path}/todolist.db') as con:
      cur = con.cursor()
      a = [[i[0], i[1]] for i in cur.execute('SELECT user_id, task FROM todolist').fetchall()]
      return a
  @todolist.setter
  def todolist(self) -> None:
    pass

  @property
  def note_list(self) -> list:
    with sq.connect(f'{self.database_path}/users.db') as con:
      cur = con.cursor()
      return [[i[0], i[1]] for i in cur.execute('SELECT user_id, note FROM users').fetchall()]
    
  @note_list.setter
  def note_list(self) -> None:
    pass

  @property
  def id_list(self) -> list:
   with sq.connect(f'{self.database_path}/users.db') as con:
      cur = con.cursor()
      result = [i[0] for i in cur.execute('SELECT user_id FROM users').fetchall()]
      return result
  
  @id_list.setter
  def id_list(self) -> None:
    pass

  def update_note(self, user_id : str, note : str) -> None:
    with sq.connect(f'{self.database_path}/users.db') as con:
      cur = con.cursor()
      cur.execute('UPDATE users SET note = ? WHERE  user_id = ?', (note, user_id,))

  def get_note(self, user_id) -> str:
    for i in self.note_list:
      if user_id == i[0]: 
        return i[1]
    return 'Нет заметки'

  def add_task(self, user_id : str, username : str, task : str) -> None:
    with sq.connect(f'{self.database_path}/todolist.db') as con:
      cur = con.cursor()
      cur.execute('INSERT INTO todolist (user_id, username, task) VALUES (?, ?, ?)', 
                  (user_id, username, task))

  def done_task(self, user_id : str, task : str) -> None:
     with sq.connect(f'{self.database_path}/todolist.db') as con:
      cur = con.cursor()
      if task[-1] == '☑':
        cur.execute('UPDATE todolist SET task = ? WHERE  task = ? AND user_id = ?', 
                    (f'{task[:-1:]}', task, user_id,))
      else: 
        cur.execute('UPDATE todolist SET task = ? WHERE  task = ? AND user_id = ?', 
                    (f'{task}☑', task, user_id,))

  def clear_done_task(self, user_id : str) -> None:
    with sq.connect(f'{self.database_path}/todolist.db') as con:
      cur = con.cursor()
      cur.execute('DELETE FROM todolist WHERE task LIKE "%☑" AND user_id = ?', (user_id,))

  def perm(self, user_id : str, perm : str) -> bool : 
    if perm == None: return True
    with sq.connect(f'{self.database_path}/users.db') as con:
      cur = con.cursor()
      if user_id in self.id_list:
        result = cur.execute(f'SELECT {perm} FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
        return bool(result)
      
  def exit(self, user_id : str) -> None:
    with sq.connect(f'{self.database_path}/users.db') as con:
      if user_id in self.id_list:
        cur = con.cursor()
        cur.execute('UPDATE users SET admin = 0 WHERE user_id = ?', (user_id,))

  def add_admin(self, user_id : str, username : str) -> bool:
    with sq.connect(f'{self.database_path}/users.db') as con:
      cur = con.cursor()
      if user_id in self.id_list:
        cur.execute('UPDATE users SET admin = 1 WHERE user_id = ?', (user_id,))
      else: 
        self.add_user_id(user_id, username)
        cur.execute('UPDATE users SET admin = 1 WHERE user_id = ?', (user_id,))
    
  def add_user_id(self, user_id : str, username : str) -> None:
      with sq.connect(f'{self.database_path}/users.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO users (user_id, username, note) VALUES (?, ?, "Нет заметки")', 
                    (user_id, username,))
        
  def add_gpt(self, user_id : str, username : str) -> None:
    if user_id not in self.id_list:
      self.add_user_id(user_id, username)
    with sq.connect(f'{self.database_path}/users.db') as con:
      cur = con.cursor()
      cur.execute('UPDATE users SET gpt = 1 WHERE user_id = ?', (user_id,))