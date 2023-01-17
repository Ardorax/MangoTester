#!/usr/bin/python3

from program.command import MangoCommand
from server.pull import pull
from server.push import push
from client.tests import run_test, local_test
from client.init import init_tests, add_test
from client.inspect import inspect
import sys


flags = {
    "verbose": False
}

commands = {
    MangoCommand("pull", ["category"], pull),
    MangoCommand("init", [], init_tests),
    MangoCommand("add", ["category", "name"], add_test),
    MangoCommand("test", ["category"], run_test),
    MangoCommand("local", ["category"], local_test),
    MangoCommand("push", [], push),
    MangoCommand("inspect", ["category"], inspect),
}

positional = list(filter(lambda command: not command.startswith("--"), sys.argv))
optional = list(filter(lambda command: command.startswith("--"),  sys.argv))

for flag in optional:
    if flag[2:] in flags:
        flags[flag[2:]] = True

if len(positional) < 2:
    print("Usage: mango <command> [args]")
    print("Available commands:")
    for command in commands:
        print(f'  - {command.name} {" ".join([f"<{arg}>" for arg in command.args])}')
    exit(1)

for command in commands:
    if command.name == positional[1]:
        if len(positional) - 2 == len(command.args):
            command.action(*positional[2:], flags)
        else:
            print(
                f'Usage: mango {command.name} {" ".join([f"<{arg}>" for arg in command.args])}'
            )
        break
