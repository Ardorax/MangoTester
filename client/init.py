import os

TEST_CONTENT = """{
    "preliminaries": [
        "gcc *.c main.c -o test"
    ],
    "tests": [
        {
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

def init_tests():
    if os.path.exists("mango"):
        print("Mango directory already exists")
        return
    os.mkdir("mango")

def add_test(category, name):
    if not os.path.exists("mango"):
        print("Mango directory does not exist")
        return
    if not os.path.exists(f"mango/{category}"):
        os.mkdir(f"mango/{category}")
    if os.path.exists(f"mango/{category}/{name}"):
        print(f"Test {name} already exists")
        return
    os.mkdir(f"mango/{category}/{name}")
    os.mkdir(f"mango/{category}/{name}/files")
    with open(f"mango/{category}/{name}/test.json", "w+") as f:
        f.write(TEST_CONTENT)