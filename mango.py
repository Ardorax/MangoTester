from command import MangoCommand
from server.example import pull
from client.tests import run_test
import sys

commands = {
    MangoCommand("pull", [], pull),
    MangoCommand("test", ["name"], run_test)
}

for command in commands:
    if command.name == sys.argv[1]:
        if len(sys.argv) - 2 == len(command.args):
            command.action(*sys.argv[2:])
        else:
            print(f'Usage: mango {command.name} {" ".join([f"<{arg}>" for arg in command.args])}')
        break
