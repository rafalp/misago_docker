import re

from email import run_email_wizard
from locale import run_locale_wizard
from utils import get_random_secret_key

FILE_HEADER = "Misago service settings"
HOSTNAME_REGEX = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)


def run_misago_wizard(env_file):
    # Disable debug by default, because it's safer that way
    env_file["MISAGO_DEBUG"] = "no"

    # Generate random secret key using Django's algorithm
    env_file["MISAGO_SECRET_KEY"] = get_random_secret_key()

    # Ask user to fill in some values
    run_address_wizard(env_file)
    run_locale_wizard(env_file)
    run_timezone_wizard(env_file)
    run_email_wizard(env_file)

    env_file.save(FILE_HEADER)
    print("Misago configuration has been saved to %s" % env_file.path)


def run_address_wizard(env_file):
    hostname_prompt = 'Enter your site\'s hostname (eg. "mysite.com"): '
    hostname = None

    while not hostname:
        hostname = input(hostname_prompt).strip().lower()
        try:
            if not hostname:
                raise ValueError("You have to enter a hostname.")
            if len(hostname) > 255:
                raise ValueError("Hostname can't be longer than 255 characters.")
            if hostname.startswith("http"):
                raise ValueError(
                    "Hostname can't include the protocol protocol name. "
                    "Please don't include the http:// or https://."
                )
            if not all(HOSTNAME_REGEX.match(x) for x in hostname.split(".")):
                raise ValueError("Entered hostname contains disallowed characters.")
        except ValueError as e:
            hostname = None

            print(e.args[0])
            print()
            print(
                "The hostname is a domain name (optionally including the subdomain) "
                'without the protocol name (eg. "http://misago.com"), '
                'port ("misago.com:443"), '
                'or path segment ("misago.com/" or "misago.com/forum/").'
            )
            print()

    env_file["VIRTUAL_HOST"] = hostname
    env_file["MISAGO_ADDRESS"] = "https://%s" % hostname


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
