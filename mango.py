from command import MangoCommand
from server.example import pull
import sys

commands = {
    MangoCommand("pull", [], pull)
}

for command in commands:
    if command.name == sys.argv[1]:
        command.action()
        break
