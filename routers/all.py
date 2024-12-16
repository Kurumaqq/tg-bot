from routers.cmd import cmd_router
from routers.cmd_text import cmd_text_router
from routers.callback_cmd import cb_router
from routers.file_handler import files_router
from routers.state import fsm_router

router_master = [cmd_router, fsm_router, cb_router, files_router, cmd_text_router]