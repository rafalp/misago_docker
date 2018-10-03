import random


def input_bool(prompt, default=True):
    if default:
        suggestion = "Y/n"
    else:
        suggestion = "N/y"

    result = None
    while result is None:
        result = input("%s [%s]: " % (prompt, suggestion))
        result = result.strip().lower()
        if result == "":
            return default
        if result not in ["y", "n"]:
            result = None
            print("Invalid choice.")
    return result == "y"


def input_choice(prompt, choices):
    result = None
    while result is None:
        result = input("%s [%s]: " % (prompt, "/".join(choices)))
        result = result.strip().lower()
        if result not in choices:
            result = None
            print("Invalid choice.")
    return result


RANDOM_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_random_string(length, allowed_chars=RANDOM_CHARS):
    return "".join(random.choice(allowed_chars) for i in range(length))


def get_random_secret_key():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return get_random_string(50, chars)
