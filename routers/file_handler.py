from routers.init import *

files_router = Router()

@files_router.message(F.content_type == ContentType.DOCUMENT)
async def download_file(msg : Message):
  file_id = msg.document.file_id
  file = await bot.get_file(file_id)
  downloaded_file = await bot.download_file(file.file_path)

  with open(f'{FILE_PATH}/{msg.document.file_name}', 'wb') as end_file: 
    end_file.write(downloaded_file.getvalue())
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)