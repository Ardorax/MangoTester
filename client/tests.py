import tempfile
import os
import subprocess
import json
from program.print import print_error
from program.message import NOT_FOUND_LOCAL, NO_TESTS_FOUND, INVALID_TEST, UNABLE_TO_RUN


def load_tests(category, local):
    temp_dir = tempfile.gettempdir()
    user_name = os.getlogin()

    if not os.path.exists("mango"):
        print_error(NOT_FOUND_LOCAL)
        return
    if not os.path.exists(f"mango/{category}"):
        print_error(NO_TESTS_FOUND.format(category=category))
    os.system(f"cp -r mango/{category}/* {temp_dir}/mango/tests")
    if local:
        for file in os.listdir(f"{temp_dir}/mango/tests"):
            if not file.startswith(f"{user_name}_"):
                os.system(f"rm -rf {temp_dir}/mango/tests/{file}")


def get_test_config(test):
    temp_dir = tempfile.gettempdir()
    with open(f"{temp_dir}/mango/tests/{test}/test.json", "r") as f:
        return json.loads(f.read())


def prepare_test(file, config):
    temp_dir = tempfile.gettempdir()
    os.system(f"rm -rf {temp_dir}/mango/tester")
    os.mkdir(f"{temp_dir}/mango/tester")
    if os.path.isdir(f"{temp_dir}/mango/tests/{file}/files") and len(os.listdir(f"{temp_dir}/mango/tests/{file}/files")) > 0:
        os.system(
            f"cp -r {temp_dir}/mango/tests/{file}/files/* {temp_dir}/mango/tester")
    os.system(f"cp -r * {temp_dir}/mango/tester")
    os.chdir(f"{temp_dir}/mango/tester")
    if "preliminaries" in config:
        for command in config["preliminaries"]:
            process = subprocess.call(
                command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if process != 0:
                print(f"\033[91mError while running \"{command}\"\033[0m")
                return False


def test_info(name, succes):
    if succes:
        print(f"\033[92m\u2713\033[0m {name}")
    else:
        print(f"\033[91m\u2717\033[0m {name}")


def unprintable(string):
    return string.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")


def assertion_error(test, type, command, expected, got):
    test_info(test, False)
    print(f"\033[90m> {command}\n{type}: Assertion failed")
    print(f"Expected \"{unprintable(expected)}\", got \"{unprintable(got)}\"\033[0m")


def run_it(test, file, name):
    if not test["assert"] or not test["command"]:
        print(f"Test {file} is not valid")
        return
    process = subprocess.Popen(test["command"].split(
    ), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    stdout, stderr = process.communicate()
    returncode = process.returncode
    if "stdout" in test["assert"] and test["assert"]["stdout"] != stdout.decode("utf-8"):
        assertion_error(
            name, "stdout", test["command"], test["assert"]["stdout"], stdout.decode("utf-8"))
        return
    if "stderr" in test["assert"] and test["assert"]["stderr"] != stderr.decode("utf-8"):
        assertion_error(
            name, "sterr", test["command"], test["assert"]["sterr"], stderr.decode("utf-8"))
        return
    if "status" in test["assert"] and test["assert"]["status"] != returncode:
        assertion_error(
            name, "status", test["command"], test["assert"]["status"], returncode)
        return
    test_info(name, True)


def runner(category, local=False):
    temp_dir = tempfile.gettempdir()
    os.system(f"rm -rf {temp_dir}/mango")
    os.mkdir(f"{temp_dir}/mango")
    os.mkdir(f"{temp_dir}/mango/tests")
    load_tests(category, local)
    files = os.listdir(f"{temp_dir}/mango/tests")
    if not files:
        print_error(NO_TESTS_FOUND.format(category=category))
        return
    for file in files:
        if not os.path.exists(f"{temp_dir}/mango/tests/{file}/test.json"):
            print_error(INVALID_TEST.format(name=file))
            continue
        working_dir=os.getcwd()
        config=get_test_config(file)
        prepare_test(file, config)

        for i, test in enumerate(config["tests"]):
            test_name=test["name"] if "name" in test else f"{file}-{i}"
            try:
                run_it(test, file, test_name)
            except Exception as e:
                test_info(test_name, False)
                print(f"\033[90m{UNABLE_TO_RUN}\033[0m")
        os.chdir(working_dir)


def local_test(category):
    runner(category, True)

def run_test(category):
    runner(category)
