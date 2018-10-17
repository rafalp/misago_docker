import re

from config import misago
from utils import input_bool, print_setup_changed_message


def run_timezone_wizard(env_file):
    timezone_prompt = (
        "Enter the TZ Database (https://bit.ly/2glGdNY) timezone name for your site "
        '(eg. "Europe/Warsaw"): '
    )
    timezone = None

    while not timezone:
        timezone = input(timezone_prompt).strip().replace("\\", "/")
        if not timezone:
            timezone = None
            print("You have to enter a timezone name.")
            print()

    env_file["MISAGO_TIME_ZONE"] = timezone


def print_timezone_setup(env_file):
    print('Using "%s" as timezone.' % env_file.get("MISAGO_TIME_ZONE"))


def change_timezone_setup(env_file):
    print_timezone_setup(misago)
    print()
    if input_bool("Change timezone configuration?", default=False):
        run_timezone_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_timezone_setup(misago)
        except KeyboardInterrupt:
            print()
