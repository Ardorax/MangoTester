import os
from program.print import print_error
from program.message import NOT_FOUND_LOCAL


def pull(category):
    if not os.path.exists("mango"):
        print_error(NOT_FOUND_LOCAL)
        return
    home_dir = os.path.expanduser("~")
    status = os.system(f"cd {home_dir}/.mango/mangodb && git pull > /dev/null 2>&1")
    user_name = os.getlogin()
    if status != 0:
        print_error("Some error happend during pull...")
        return
    if not os.path.exists(f"{home_dir}/.mango/mangodb/{category}"):
        print_error(f"Category {category} does not exist on server")
        return
    if not os.path.exists(f"mango/{category}"):
        os.mkdir(f"mango/{category}")
    for file in os.listdir(f"mango/{category}"):
        if not file.startswith(f"{user_name}_"):
            os.system(f"rm -rf mango/{category}/{file}")
    os.system(f"rm -rf {home_dir}/.mango/mangodb/{category}/{user_name}_*")
    os.system(f"cp -r {home_dir}/.mango/mangodb/{category}/* mango/{category}")