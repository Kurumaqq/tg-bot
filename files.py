from cfg import FILE_PATH
from os import listdir
from os.path import isfile, join

def get_file_path() -> tuple[str]:
  return ((f"{FILE_PATH}/{f}") 
          for f in 
          listdir(FILE_PATH) 
          if isfile(join(FILE_PATH, f)))