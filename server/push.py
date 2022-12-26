import os
import sys

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
    os.system(f"cd {mango_db} && git pull && git push")
