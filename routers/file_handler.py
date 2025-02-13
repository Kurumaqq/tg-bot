from routers.imports import *

files_router = Router()

@files_router.message(F.content_type == ContentType.DOCUMENT)
async def download_file(msg : Message):
  user = User_properties(msg)
  if users_db.check_perm(user.id, 'admin'):
    file_id = msg.document.file_id
    file = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file.file_path)

    with open(f'{FILE_PATH}/{msg.document.file_name}', 'wb') as final_file: 
      final_file.write(downloaded_file.getvalue())
      await bot.delete_message(chat_id=user.chat_id, message_id=user.msg_id)

@files_router.message(F.content_type == ContentType.PHOTO)
async def rem_bg_photo(msg : Message):
  user = User_properties(msg)
  bot_msg = await msg.answer('Подождите...')
  photo = await bot.get_file(msg.photo[-1].file_id)
  photo_name = f'kurumaka_photo_{randint(1, 999)}.png'

  await bot.download_file(photo.file_path, photo_name)
  with open(photo_name, 'rb') as input_file: input_image = remove(input_file.read())
  with open(photo_name, 'wb') as output_file: output_file.write(input_image)
    
  await del_msg(bot_msg=bot_msg, user_msg=msg)
  await bot.send_chat_action(chat_id=user.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
  await msg.answer_document(FSInputFile(photo_name))
  os.remove(photo_name)