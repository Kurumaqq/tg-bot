from dotenv import load_dotenv
from os import getenv

load_dotenv()
class Config():
    @property
    def token(self) -> str:
        return getenv('TOKEN')

    @property
    def password(self) -> str:
        return getenv('PASSWORD')
    
    @property
    def own_chat_id(self) -> str:
        return getenv('OWN_CHAT_ID')
    
    @property
    def commands(self) -> dict[dict]:
        return {
        '/help': {'desc': 'все команды', 'perm': None},
        '/flip': {'desc': 'подкинуть монетку', 'perm': None}, 
        '/gen': {'desc': 'сгенерировать пароль', 'perm': None},
        '/exit': {'desc': 'забыть пользователя', 'perm': 'admin'},
        '/allpass': {'desc': 'отправить все пароли', 'perm': 'admin'},
        'p [app]': {'desc': 'пароль от приложения', 'perm': 'admin'},
        'p- [app]': {'desc': 'удалить пароль', 'perm': 'admin'},
        'p+ [app] [password]': {'desc': 'добавить пароль', 'perm': 'admin'},
        }
