import re

from config import misago
from utils import get_random_string, input_bool, print_setup_changed_message


def get_random_secret_key():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return get_random_string(50, chars)


def set_random_secret_key(env_file):
    env_file["MISAGO_SECRET_KEY"] = get_random_secret_key()


def print_secret_key(env_file):
    print("Secret key: %s" % env_file.get("MISAGO_SECRET_KEY"))


def reset_secret_key(env_file):
    print_secret_key(misago)
    print()
    if input_bool("Generate new secret key?", default=False):
        set_random_secret_key(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            reset_secret_key(misago)
        except KeyboardInterrupt:
            print()
