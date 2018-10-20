import re

from config import misago
from utils import BOOL_TRUE, input_bool, print_setup_changed_message


def run_facebook_signin_wizard(env_file):
    if input_bool("Enable sign-in with Facebook?"):
        run_facebook_key_wizard(env_file)
        run_facebook_secret_wizard(env_file)
        env_file["SOCIAL_AUTH_FACEBOOK_ENABLE"] = "yes"
    else:
        env_file["SOCIAL_AUTH_FACEBOOK_ENABLE"] = "no"


def run_facebook_key_wizard(env_file):
    facebook_key_prompt = "Enter your Facebook App ID: "
    facebook_key = None

    while not facebook_key:
        facebook_key = input(facebook_key_prompt).strip().lower()
        if not facebook_key:
            print("You have to enter a Facebook App ID.")
            print()

    env_file["SOCIAL_AUTH_FACEBOOK_KEY"] = facebook_key


def run_facebook_secret_wizard(env_file):
    facebook_secret_prompt = "Enter your Facebook App Secret: "
    facebook_secret = None

    while not facebook_secret:
        facebook_secret = input(facebook_secret_prompt).strip().lower()
        if not facebook_secret:
            print("You have to enter a Facebook App Secret.")
            print()

    env_file["SOCIAL_AUTH_FACEBOOK_SECRET"] = facebook_secret


def print_facebook_signin_setup(env_file):
    if env_file.get("SOCIAL_AUTH_FACEBOOK_ENABLE") in BOOL_TRUE:
        print("Sign-in with Facebook is enabled:")
        print()
        print("App ID:      %s" % env_file.get("SOCIAL_AUTH_FACEBOOK_KEY"))
        print("App Secret:  %s" % env_file.get("SOCIAL_AUTH_FACEBOOK_SECRET"))
    else:
        print("Sign-in with Facebook is disabled.")


def change_facebook_signin_setup(env_file):
    print_facebook_signin_setup(misago)
    print()
    if input_bool("Change sign-in with Facebook setup?", default=False):
        run_facebook_signin_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_facebook_signin_setup(misago)
        except KeyboardInterrupt:
            print()
