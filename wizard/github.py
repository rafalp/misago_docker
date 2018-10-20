import re

from config import misago
from utils import BOOL_TRUE, input_bool, print_setup_changed_message


def run_github_signin_wizard(env_file):
    if input_bool("Enable sign-in with GitHub?"):
        run_github_key_wizard(env_file)
        run_github_secret_wizard(env_file)
        env_file["SOCIAL_AUTH_GITHUB_ENABLE"] = "yes"
    else:
        env_file["SOCIAL_AUTH_GITHUB_ENABLE"] = "no"


def run_github_key_wizard(env_file):
    github_key_prompt = "Enter your GitHub Client ID: "
    github_key = None

    while not github_key:
        github_key = input(github_key_prompt).strip().lower()
        if not github_key:
            print("You have to enter a GitHub Client ID.")
            print()

    env_file["SOCIAL_AUTH_GITHUB_KEY"] = github_key


def run_github_secret_wizard(env_file):
    github_secret_prompt = "Enter your GitHub Client Secret: "
    github_secret = None

    while not github_secret:
        github_secret = input(github_secret_prompt).strip().lower()
        if not github_secret:
            print("You have to enter a GitHub Client Secret.")
            print()

    env_file["SOCIAL_AUTH_GITHUB_SECRET"] = github_secret


def print_github_signin_setup(env_file):
    if env_file.get("SOCIAL_AUTH_GITHUB_ENABLE") in BOOL_TRUE:
        print("Sign-in with GitHub is enabled:")
        print()
        print("Client ID:       %s" % env_file.get("SOCIAL_AUTH_GITHUB_KEY"))
        print("Client Secret:   %s" % env_file.get("SOCIAL_AUTH_GITHUB_SECRET"))
    else:
        print("Sign-in with GitHub is disabled.")


def change_github_signin_setup(env_file):
    print_github_signin_setup(misago)
    print()
    if input_bool("Change sign-in with GitHub setup?", default=False):
        run_github_signin_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_github_signin_setup(misago)
        except KeyboardInterrupt:
            print()
