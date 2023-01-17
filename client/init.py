import os
from program.print import print_error
from program.message import ALREADY_EXISTS, NOT_FOUND_LOCAL, TEST_ALREADY_EXISTS

TEST_CONTENT = """{
    "preliminaries": [
        "gcc *.c main.c -o test"
    ],
    "tests": [
        {
            "name": "Test 1",
            "command": "./test 1 2 3",
            "assert": {
                "stdout": "6\\n",
                "stderr": "",
                "status": 0
            }
        }
    ]
}
"""

def init_tests(flags):
    if os.path.exists("mango"):
        print_error(ALREADY_EXISTS)
        return
    os.mkdir("mango")

def add_test(category, name, flags):
    user_name = os.getlogin()
    if not os.path.exists("mango"):
        print_error(NOT_FOUND_LOCAL)
        return
    if not os.path.exists(f"mango/{category}"):
        os.mkdir(f"mango/{category}")
    if os.path.exists(f"mango/{category}/{user_name}_{name}"):
        print_error(TEST_ALREADY_EXISTS.format(name=name))
        return
    os.mkdir(f"mango/{category}/{user_name}_{name}")
    os.mkdir(f"mango/{category}/{user_name}_{name}/files")
    with open(f"mango/{category}/{user_name}_{name}/test.json", "w+") as f:
        f.write(TEST_CONTENT)