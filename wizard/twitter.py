import re

from config import misago
from utils import BOOL_TRUE, input_bool, print_setup_changed_message


def run_twitter_signin_wizard(env_file):
    if input_bool("Enable sign-in with Twitter?"):
        run_twitter_key_wizard(env_file)
        run_twitter_secret_wizard(env_file)
        env_file["SOCIAL_AUTH_TWITTER_ENABLE"] = "yes"
    else:
        env_file["SOCIAL_AUTH_TWITTER_ENABLE"] = "no"


def run_twitter_key_wizard(env_file):
    twitter_key_prompt = "Enter your Twitter Consumer ID: "
    twitter_key = None

    while not twitter_key:
        twitter_key = input(twitter_key_prompt).strip().lower()
        if not twitter_key:
            print("You have to enter a Twitter Consumer ID.")
            print()

    env_file["SOCIAL_AUTH_TWITTER_KEY"] = twitter_key


def run_twitter_secret_wizard(env_file):
    twitter_secret_prompt = "Enter your Twitter Consumer Secret: "
    twitter_secret = None

    while not twitter_secret:
        twitter_secret = input(twitter_secret_prompt).strip().lower()
        if not twitter_secret:
            print("You have to enter a Twitter Consumer Secret.")
            print()

    env_file["SOCIAL_AUTH_TWITTER_SECRET"] = twitter_secret


def print_twitter_signin_setup(env_file):
    if env_file.get("SOCIAL_AUTH_TWITTER_ENABLE") in BOOL_TRUE:
        print("Sign-in with Twitter is enabled:")
        print()
        print("Consumer ID:       %s" % env_file.get("SOCIAL_AUTH_TWITTER_KEY"))
        print("Consumer Secret:   %s" % env_file.get("SOCIAL_AUTH_TWITTER_SECRET"))
    else:
        print("Sign-in with Twitter is disabled.")


def change_twitter_signin_setup(env_file):
    print_twitter_signin_setup(misago)
    print()
    if input_bool("Change sign-in with Twitter setup?", default=False):
        run_twitter_signin_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_twitter_signin_setup(misago)
        except KeyboardInterrupt:
            print()
