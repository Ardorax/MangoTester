import os

def pull():
    print("Commande de pull")
    status = os.system("cd ~/.mango/mangodb && git pull && exit 22")
    if status // 256 == 22:
        print("Pull executed sucessfully !")
    else:
        print("Some error happend during pull...")