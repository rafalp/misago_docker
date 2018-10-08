import re

from env import misago
from utils import input_bool, input_choice, print_setup_changed_message

SENTRY_DSN_REGEX = re.compile(r"^https://[0-9a-z]+(:[0-9a-z]+)?@sentry\.io/[0-9]+$")


def run_sentry_wizard(env_file):
    if input_bool("Enable Sentry logging?"):
        run_dsn_wizard(env_file)
        run_logging_level_wizard(env_file)
    else:
        disable_sentry(env_file)


def disable_sentry(env_file):
    env_file["SENTRY_DSN"] = ""
    env_file["SENTRY_LEVEL"] = ""


def run_dsn_wizard(env_file):
    sentry_dsn_prompt = "Enter your Sentry DSN: "
    sentry_dsn = None

    while not sentry_dsn:
        sentry_dsn = input(sentry_dsn_prompt).strip().lower()
        try:
            if not sentry_dsn:
                raise ValueError("You have to enter a Sentry DSN.")
            if not SENTRY_DSN_REGEX.match(sentry_dsn):
                raise ValueError("Entered value is not a valid Sentry DSN.")
        except ValueError as e:
            sentry_dsn = None
            print(e.args[0])
            print()

    env_file["SENTRY_DSN"] = sentry_dsn


def run_logging_level_wizard(env_file):
    logging_level_prompt = [
        "Which e-mail provider do you want to use?",
        "",
        "1 - DEBUG",
        "2 - INFO (recommended)",
        "3 - WARNING",
        "4 - ERROR",
        "5 - CRITICAL",
        "",
        "Enter choice's number",
    ]

    logging_level = input_choice(
        "\n".join(logging_level_prompt), "12345", coerce_to=int
    )

    choices_values = {1: "DEBUG", 2: "INFO", 3: "WARNING", 4: "ERROR", 5: "CRITICAL"}

    env_file["SENTRY_LEVEL"] = choices_values[logging_level]


def print_sentry_setup(env_file):
    if env_file.get("SENTRY_DSN"):
        print("Logging to Sentry is enabled:")
        print()
        print("DSN:     %s" % env_file.get("SENTRY_DSN"))
        print("Level:   %s" % env_file.get("SENTRY_LEVEL", "ERROR"))
    else:
        print("Logging to Sentry is disabled.")


def change_sentry_setup(env_file):
    print_sentry_setup(misago)
    print()
    if input_bool("Change Sentry logging?", default=False):
        run_sentry_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_sentry_setup(misago)
        except KeyboardInterrupt:
            print()
