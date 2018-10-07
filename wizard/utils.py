import random

BOOL_TRUE = ("y", "yes", "true", "1")


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


def input_choice(prompt, choices, coerce_to=str):
    result = None
    while result is None:
        result = input("%s [%s]: " % (prompt, "/".join(choices)))
        result = result.strip().lower()
        if result not in choices:
            result = None
            print("Invalid choice.")
    return coerce_to(result)


RANDOM_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_random_string(length, allowed_chars=RANDOM_CHARS):
    return "".join(random.choice(allowed_chars) for i in range(length))


def get_bool_display(value):
    if value in BOOL_TRUE:
        return "Yes"
    return "No"


def serialize_bool(value):
    if value:
        return "yes"
    return "no"


def print_setup_changed_message():
    print(
        "Changes saved. "
        'Remember to run "./appctl rebuild" to rebuild and restart '
        "Misago container to use new configuration."
    )
