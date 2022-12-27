import os
import sys
from program.print import print_error
from program.message import NOT_FOUND_LOCAL, NOT_FOUND_SYS

mango_db = os.path.expanduser("~/.mango/mangodb")
mango_local = "./mango"


def remove_folder(path: str):
    if ".." in path:
        return 1
    # print("delete", path)
    os.system(f"rm -rf {path}")


def delete_user_tests(category: str):
    name = os.getlogin() + "_"
    for test in os.listdir(os.path.join(mango_db, category)):
        if test.startswith(name):
            remove_folder(os.path.join(mango_db, category, test))


def push():
    # For all the category on the mango folder
    if (not os.path.exists(mango_local)):
        print_error(NOT_FOUND_LOCAL)
        return
    if (not os.path.exists(mango_db)):
        print_error(NOT_FOUND_SYS)
        return
    for category in os.listdir(mango_local):
        category_folder = os.path.join(mango_local, category)
        # Ignore files
        if not os.path.isdir(category_folder):
            continue
        
        print("On category:", category)

        # If category don't exist on remote:
        if not os.path.exists(os.path.join(mango_db, category)):
            # Create it.
            os.mkdir(os.path.join(mango_db, category))
        else:
            # Delete all old tests.
            delete_user_tests(category)
        
        # Put all the new tests on the remote
        for test in os.listdir(category_folder):
            test_folder = os.path.join(category_folder, test)
            print("-", test)
            os.system(f"cp -r {test_folder} {os.path.join(mango_db, category, test)}")
    
    # Update remote db
    status = os.system(f"cd {mango_db} && git pull && git add --all && git commit -m \"autocommit\" && git push")
    if status != 0:
        print_error("Some error happend during push...")
        return
    print("\033[92m", end="")
    print("\u2713", end=" ")
    print("Pushed successfully!")
