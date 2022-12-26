import os

def pull():
    print("Commande de pull")
    # TODO verify the pull append correctly
    print(os.system("cd ~/.mango/mangodb && git pull"))