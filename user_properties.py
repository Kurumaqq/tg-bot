from aiogram.types import Message, CallbackQuery

class User_properties():
    def __init__(self, user : Message | CallbackQuery):
        self.name = user.from_user.username
        self.id = str(user.from_user.id)
        self.id_int = user.from_user.id

        if isinstance(user, Message):
            self.msg_id = user.message_id
            self.chat_id = user.chat.id
          
        elif isinstance(user, CallbackQuery):
            self.msg_id = user.message.message_id
            self.chat_id = user.message.chat.id
        else: raise TypeError
            
