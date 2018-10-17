import re

from config import misago
from utils import input_bool, print_setup_changed_message

LOCALE_REGEX = re.compile(r"^[a-z]{2,3}(-[a-z]+)?$", re.IGNORECASE)
LANGUAGE_SEARCH_CONFIGS = {
    "en": "english",
    "nl": "dutch",
    "fi": "finnish",
    "fr": "french",
    "de": "german",
    "hu": "hungarian",
    "it": "italian",
    "no": "norwegian",
    "nb": "norwegian",
    "nn": "norwegian",
    "pt": "portuguese",
    "ro": "romanian",
    "ru": "russian",
    "es": "spanish",
    "sv": "swedish",
    "tt": "turkish",
}


def run_locale_wizard(env_file):
    locale_prompt = (
        'Enter the language code for your site\'s locale (eg. "pl" or "en-us"): '
    )
    locale = None

    while not locale:
        locale = input(locale_prompt).strip().lower().replace("_", "-")
        try:
            if not locale:
                raise ValueError("You have to enter a language code.")
            if not LOCALE_REGEX.match(locale):
                raise ValueError("This is not a valid language code.")
        except ValueError as e:
            locale = None
            print(e.args[0])
            print()

    env_file["MISAGO_LANGUAGE_CODE"] = locale

    search_config_name = locale[:2]
    if search_config_name in LANGUAGE_SEARCH_CONFIGS:
        env_file["MISAGO_SEARCH_CONFIG"] = LANGUAGE_SEARCH_CONFIGS[search_config_name]
    else:
        # fallback to "simple" config
        env_file["MISAGO_SEARCH_CONFIG"] = "simple"


def print_locale_setup(env_file):
    settings = (
        env_file.get("MISAGO_LANGUAGE_CODE"),
        env_file.get("MISAGO_SEARCH_CONFIG", "simple"),
    )
    print('Using "%s" locale and "%s" search config.' % settings)


def change_locale_setup(env_file):
    print_locale_setup(misago)
    print()
    if input_bool("Change locale configuration?", default=False):
        run_locale_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_locale_setup(misago)
        except KeyboardInterrupt:
            print()
