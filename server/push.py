import os
import sys

# TODO
def send_test():
    pass

def push():
    mangoFolder = "./mango"
    mangoDb = "~/.mango/mangodb"
    print("push new tests")
    if not os.path.exists(mangoFolder):
        print("mango folder not found.", file=sys.stderr)
        return 1
    for category in os.listdir(mangoFolder):
        # Ignore files
        categoryFolder = os.path.join(mangoFolder, category)
        if not os.path.isdir(categoryFolder):
            continue
        print(category)
        for test in os.listdir(categoryFolder):
            testFolder = os.path.join(categoryFolder, test)
            if not os.path.isdir(testFolder):
                continue
            send_test()
