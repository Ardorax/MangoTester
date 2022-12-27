import os
from .print import print_error
from .message import NOT_FOUND_LOCAL, NOT_FOUND_SYS

mango_db = os.path.expanduser("~/.mango/mangodb")

def has_mango_folder():
    if not os.path.exists("mango"):
        print_error(NOT_FOUND_LOCAL)
        return False
    return True

def has_mango_db():
    if not os.path.exists(mango_db):
        print_error(NOT_FOUND_SYS)
        return False
    return True