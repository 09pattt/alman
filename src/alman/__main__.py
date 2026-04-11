from alman.app import cli
from alman.app import router

def entry_point():
    router.args_handler(cli.main())