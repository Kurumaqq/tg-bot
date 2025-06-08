from src.routers.comand_handler import cmd_router
from src.routers.text_handler import cmd_text_router
from src.routers.callback_handler import cb_router

router_master = [cmd_router, cb_router, cmd_text_router]
