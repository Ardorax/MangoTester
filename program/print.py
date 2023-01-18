def print_error(error):
    print("\033[91m", end="")
    print("\u2717", end=" ")
    print(error, end="")
    print("\033[0m")


def print_successful(msg):
    print(f"\033[92m\u2713 {msg}\033[0m")
