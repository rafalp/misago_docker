import re

from utils import get_random_secret_key, input_bool, input_choice

FILE_HEADER = "Misago service settings"
HOSTNAME_REGEX = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
LANGUAGE_REGEX = re.compile(r"^[a-z]{2,3}(-[a-z]+)?$", re.IGNORECASE)
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


def run_misago_wizard(env_file):
    # Disable debug by default, because it's safer that way
    env_file["DEBUG"] = "no"

    # Generate random secret key using Django's algorithm
    env_file["SECRET_KEY"] = get_random_secret_key()

    # Ask user to fill in some values
    run_address_wizard(env_file)
    run_language_wizard(env_file)
    run_timezone_wizard(env_file)
    run_email_wizard(env_file)

    env_file["SENDINBLUE_API_KEY"] = "fixme"
    env_file["SENTRY_DSN"] = "fixme"

    env_file.save(FILE_HEADER)


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


def run_language_wizard(env_file):
    language_prompt = (
        'Enter the language code for your site\'s locale (eg. "pl" or "en-us"): '
    )
    language = None

    while not language:
        language = input(language_prompt).strip().lower().replace("_", "-")
        try:
            if not language:
                raise ValueError("You have to enter a language.")
            if not LANGUAGE_REGEX.match(language):
                raise ValueError("This is not a valid language code.")
        except ValueError as e:
            language = None
            print(e.args[0])
            print()

    env_file["LANGUAGE_CODE"] = language

    search_config_name = language[:2]
    if search_config_name in LANGUAGE_SEARCH_CONFIGS:
        env_file["SEARCH_CONFIG"] = LANGUAGE_SEARCH_CONFIGS[search_config_name]
    else:
        # fallback to "simple" config
        env_file["SEARCH_CONFIG"] = "simple"


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

    env_file["TIME_ZONE"] = timezone


def run_email_wizard(env_file):
    email_prompt = "Configure e-mail sending?"
    if not input_bool(email_prompt):
        env_file["EMAIL_PROVIDER"] = "console"
        return

    run_email_provider_wizard(env_file)


def run_email_provider_wizard(env_file):
    email_provider_prompt = [
        "Which e-mail provider do you want to use?",
        "",
        "1 - Any SMTP provider",
        "2 - Gmail (gmail.com)",
        "3 - Mailgun (mailgun.com)",
        "4 - Mailjet (mailjet.com)",
        "5 - SendinBlue (sendinblue.com/)",
        "",
        "Enter choice's number",
    ]

    email_provider = input_choice("\n".join(email_provider_prompt), "12345")

    wizards_map = {
        1: run_smtp_wizard,
        2: run_gmail_wizard,
        3: run_mailgun_wizard,
        4: run_mailjet_wizard,
        5: run_mailgun_wizard,
    }

    email_provider_wizard = wizards_map[int(email_provider)]
    email_provider_wizard(env_file)


def run_smtp_wizard(env_file):
    email_host_prompt = 'Enter your SMTP host (eg. "smtp.myprovider.com"): '
    email_host = None

    while not email_host:
        email_host = input(email_host_prompt).strip()
        if not email_host:
            email_host = None
            print("You have to enter a SMTP host.")
            print()

    email_user_prompt = "Enter your SMTP user name: "
    email_user = None

    while not email_user:
        email_user = input(email_user_prompt).strip()
        if not email_user:
            email_user = None
            print("You have to enter a SMTP user name.")
            print()

    email_password_prompt = "Enter your SMTP user password (optinal but recommended): "
    email_password = None

    while not email_password:
        email_password = input(email_password_prompt).strip()

    email_ssl = input_bool("Enable SSL")
    email_tls = input_bool("Enable TLS")

    email_password_prompt = "Enter your SMTP port: "
    email_password = None

    while not email_password:
        email_password = input(email_password_prompt).strip()

    env_file["EMAIL_PROVIDER"] = "smtp"
    env_file["EMAIL_HOST"] = email_host
    env_file["EMAIL_HOST_USER"] = email_user
    env_file["EMAIL_HOST_PASSWORD"] = email_password
    # EMAIL_USE_SSL
    # EMAIL_USE_TLS
    # EMAIL_HOST
    # EMAIL_HOST_PASSWORD
    # EMAIL_HOST_USER
    # EMAIL_PORT
    pass


def run_gmail_wizard(env_file):
    email_address_prompt = "Enter your Gmail e-mail address: "
    email_address = None

    while not email_address:
        email_address = input(email_address_prompt).strip()
        if not email_address:
            email_address = None
            print("You have to enter an e-mail address.")
            print()

    password_prompt = "Enter your Gmail password: "
    password = None

    while not password:
        password = input(password_prompt).strip()
        if not password:
            password = None
            print("You have to enter a password.")
            print()

    email_from_prompt = 'Enter your sender name (eg. "Misago Forums", optional): '
    email_from = input(email_from_prompt).strip()

    env_file["EMAIL_PROVIDER"] = "gmail"
    env_file["GMAIL_USER"] = email_address
    env_file["GMAIL_PASSWORD"] = password
    if email_from:
        env_file["DEFAULT_FROM_EMAIL"] = "%s <%s>" % (email_from, email_address)
    else:
        env_file["DEFAULT_FROM_EMAIL"] = email_address


def run_mailgun_wizard(env_file):
    api_key_prompt = "Enter your Mailgun api key: "
    api_key = None

    while not api_key:
        api_key = input(api_key_prompt).strip()
        if not api_key:
            api_key = None
            print("You have to enter an api key.")
            print()

    env_file["EMAIL_PROVIDER"] = "mailgun"
    env_file["MAILGUN_API_KEY"] = api_key


def run_mailjet_wizard(env_file):
    api_key_prompt = "Enter your Mailjet api key: "
    api_key = None

    while not api_key:
        api_key = input(api_key_prompt).strip()
        if not api_key:
            api_key = None
            print("You have to enter an api key.")
            print()

    api_secret_prompt = "Enter your Mailjet secret key: "
    api_secret = None

    while not api_secret:
        api_secret = input(api_secret_prompt).strip()
        if not api_secret:
            api_secret = None
            print("You have to enter an secret key.")
            print()

    env_file["EMAIL_PROVIDER"] = "mailjet"
    env_file["MAILJET_API_KEY_PUBLIC"] = api_key
    env_file["MAILJET_API_KEY_PRIVATE"] = api_secret
