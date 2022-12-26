import tempfile
import os
import subprocess
import json


def load_tests(category):
    temp_dir = tempfile.gettempdir()
    home_dir = os.path.expanduser("~")

    if not os.path.exists(f"{home_dir}/.mango/mangodb"):
        print("Cannot find mango on your system")
        return
    if not os.path.exists("mango"):
        print("Cannot find mango in your current directory")
        return
    if os.path.exists(f"{home_dir}/.mango/mangodb/{category}"):
        os.system(
            f"cp -r {home_dir}/.mango/mangodb/{category}/* {temp_dir}/mango/tests")
    if os.path.exists(f"mango/{category}"):
        os.system(f"cp -r mango/{category}/* {temp_dir}/mango/tests")


def get_test_config(test):
    temp_dir = tempfile.gettempdir()
    with open(f"{temp_dir}/mango/tests/{test}/test.json", "r") as f:
        return json.loads(f.read())


def prepare_test(file, config):
    temp_dir = tempfile.gettempdir()
    os.system(f"rm -rf {temp_dir}/mango/tester")
    os.mkdir(f"{temp_dir}/mango/tester")
    if os.path.exists(f"{temp_dir}/mango/tests/{file}/files"):
        os.system(
            f"cp -r {temp_dir}/mango/tests/{file}/files/* {temp_dir}/mango/tester")
    os.system(f"cp -r * {temp_dir}/mango/tester")
    os.chdir(f"{temp_dir}/mango/tester")
    if config["preliminaries"]:
        for command in config["preliminaries"]:
            process = subprocess.call(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
    print(f"\033[90m", end="")
    print(f"> {command}")
    print(f"{type}: Assertion failed")
    print(f"Expected \"{unprintable(expected)}\", got \"{unprintable(got)}\"")
    print("\033[0m", end="")


def run_it(test, file, name):
    if not test["assert"] or not test["command"]:
        print(f"Test {file} is not valid")
        return
    process = subprocess.Popen(test["command"].split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    stdout, stderr = process.communicate()
    returncode = process.returncode
    if test["assert"]["stdout"] != stdout.decode("utf-8"):
        assertion_error(name, "stdout", test["command"], test["assert"]["stdout"], stdout.decode("utf-8"))
        return
    if test["assert"]["stderr"] != stderr.decode("utf-8"):
        assertion_error(name, "sterr", test["command"], test["assert"]["sterr"], stderr.decode("utf-8"))
        return
    if test["assert"]["status"] != returncode:
        assertion_error(name, "status", test["command"], test["assert"]["status"], returncode)
        return
    test_info(name, True)

def run_test(category):
    temp_dir = tempfile.gettempdir()
    os.system(f"rm -rf {temp_dir}/mango")
    os.mkdir(f"{temp_dir}/mango")
    os.mkdir(f"{temp_dir}/mango/tests")
    load_tests(category)
    files = os.listdir(f"{temp_dir}/mango/tests")
    if not files:
        print(f"No tests found for category {category}")
        return
    for file in files:
        if not os.path.exists(f"{temp_dir}/mango/tests/{file}/test.json"):
            print(f"Test {file} is not valid")
            continue
        working_dir = os.getcwd()
        config = get_test_config(file)
        prepare_test(file, config)

        for i, test in enumerate(config["tests"]):
            try:
                run_it(test, file, f"{file}-{i}")
            except Exception as e:
                test_info(f"{file}-{i}", False)
                print(f"\033[90m", end="")
                print("Unable to run test...")
                print("\033[0m", end="")
        os.chdir(working_dir)
