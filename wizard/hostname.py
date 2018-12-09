import os
import re
from pathlib import Path

from config import VHOSTD_DIR, misago
from nginx import run_nginx_wizard
from utils import input_bool, print_setup_changed_message

HOSTNAME_REGEX = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)


def run_hostname_wizard(env_file):
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

    if hostname.startswith("www."):
        env_file["VIRTUAL_HOST"] = "%s,%s" % (hostname, hostname[4:])
    else:
        env_file["VIRTUAL_HOST"] = "{0},www.{0}".format(hostname)

    env_file["MISAGO_ADDRESS"] = "https://%s/" % hostname

    run_nginx_wizard(env_file)
    run_lets_encrypt_wizard(env_file)


def run_lets_encrypt_wizard(env_file):
    email_prompt = "Enter contact e-mail address for Let's Encrypt: "
    email = None
    while not email:
        email = input(email_prompt).strip()
        if not email or "@" not in email:
            print("You have to enter an e-mail address.")
            print()

    env_file["LETSENCRYPT_EMAIL"] = email


def print_hostname_setup(env_file):
    hostnames = [i.strip() for i in env_file.get("VIRTUAL_HOST", "").split(",")]
    hostname, redirect = hostnames

    redirect_set = Path(os.path.join(VHOSTD_DIR, redirect)).is_file()

    print("Current hostname:        %s" % hostname)
    print("Redirect from:           %s" % (redirect if redirect_set else "not set"))
    print("Let's Encrypt e-mail:    %s" % env_file.get("LETSENCRYPT_EMAIL"))


def change_hostname_setup(env_file):
    print_hostname_setup(misago)
    print()
    if input_bool("Change hostname?", default=False):
        run_hostname_wizard(env_file)
        env_file.save()
        print_setup_changed_message()
    elif run_nginx_wizard(env_file):
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_hostname_setup(misago)
        except KeyboardInterrupt:
            print()
