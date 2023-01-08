import os
import json
from program.print import print_error
from program.message import NOT_FOUND_LOCAL, NO_TESTS_FOUND, INVALID_TEST, UNABLE_TO_RUN


def inspect(category):
    files = os.listdir(f"mango/{category}")
    for fileName in files:
        if not os.path.exists(f"./mango/{category}/{fileName}/test.json"):
            print_error(INVALID_TEST.format(name=fileName))
            continue
        with open(f"./mango/{category}/{fileName}/test.json") as file:
            data = json.load(file)
            preliminaries = ""
            tests = []
            if data["preliminaries"]:
                preliminaries = "\n".join(data["preliminaries"])
            for test in data["tests"]:
                tests.append(test["command"])
            tests = "\n\t".join(tests)
            print(f"For test {fileName}:\n{preliminaries}\n\t{tests}")
