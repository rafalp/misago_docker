from config import misago
from utils import BOOL_TRUE, input_bool, print_setup_changed_message, serialize_bool


def print_debug_setup(env_file):
    if env_file.get("MISAGO_DEBUG", "").lower() in BOOL_TRUE:
        print("Debug mode is enabled.")
    else:
        print("Debug mode is disabled.")


def change_debug_setup(env_file):
    print_debug_setup(misago)
    print()
    if input_bool("Change debug mode?", default=False):
        new_debug_mode = env_file.get("MISAGO_DEBUG", "").lower() not in BOOL_TRUE
        env_file["MISAGO_DEBUG"] = serialize_bool(new_debug_mode)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_debug_setup(misago)
        except KeyboardInterrupt:
            print()
