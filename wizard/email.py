from config import misago
from utils import (
    get_bool_display,
    input_bool,
    input_choice,
    print_setup_changed_message,
    serialize_bool,
)

PROVIDER_CONSOLE = "console"
PROVIDER_GMAIL = "gmail"
PROVIDER_MAILJET = "mailjet"
PROVIDER_SENDINBLUE = "sendinblue"
PROVIDER_SMTP = "smtp"


def run_email_wizard(env_file):
    email_provider_prompt = [
        "Which e-mail provider do you want to use?",
        "",
        "0 - None (disables sending e-mails)",
        "1 - SMTP",
        "2 - Gmail (gmail.com)",
        "3 - Mailjet (mailjet.com)",
        "4 - SendinBlue (sendinblue.com)",
        "",
        "Enter choice's number",
    ]

    email_provider = input_choice(
        "\n".join(email_provider_prompt), "012345", coerce_to=int
    )

    choices_values = {
        0: disable_sending_emails,
        1: run_smtp_wizard,
        2: run_gmail_wizard,
        3: run_mailjet_wizard,
        4: run_sendinblue_wizard,
    }

    email_provider_wizard = choices_values[email_provider]
    email_provider_wizard(env_file)


def disable_sending_emails(env_file):
    env_file["MISAGO_EMAIL_PROVIDER"] = PROVIDER_CONSOLE


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
    email_password = input(email_password_prompt).strip()

    email_ssl = input_bool("Enable SSL", default=False)
    email_tls = input_bool("Enable TLS", default=False)

    email_port_prompt = "Enter your SMTP port: "
    email_port = None

    while not email_port:
        email_port = input(email_port_prompt).strip()
        if not email_port:
            email_port = None
            print("You have to enter a SMTP port.")
            print()

    email_address_prompt = "Enter your site's e-mail address: "
    email_address = input(email_address_prompt).strip()

    while not email_address:
        email_address = input(email_address_prompt).strip()
        if not email_address:
            email_address = None
            print("You have to enter e-mail address.")
            print()

    email_from_prompt = 'Enter your sender name (eg. "Misago Forums", optional): '
    email_from = input(email_from_prompt).strip()

    env_file["MISAGO_EMAIL_PROVIDER"] = PROVIDER_SMTP
    env_file["MISAGO_EMAIL_HOST"] = email_host
    env_file["MISAGO_EMAIL_PORT"] = email_port
    env_file["MISAGO_EMAIL_USER"] = email_user
    env_file["MISAGO_EMAIL_PASSWORD"] = email_password
    env_file["MISAGO_EMAIL_USE_SSL"] = serialize_bool(email_ssl)
    env_file["MISAGO_EMAIL_USE_TLS"] = serialize_bool(email_tls)

    if email_from:
        env_file["MISAGO_DEFAULT_FROM_EMAIL"] = "%s <%s>" % (email_from, email_address)
    else:
        env_file["MISAGO_DEFAULT_FROM_EMAIL"] = email_address


def run_gmail_wizard(env_file):
    email_address_prompt = "Enter your Gmail e-mail address: "
    email_address = None

    while not email_address:
        email_address = input(email_address_prompt).strip()
        if not email_address:
            email_address = None
            print("You have to enter an e-mail address.")
            print()

    print()
    print(
        "Gmail requires that each application connecting to its servers "
        "uses dedicated password."
    )
    print(
        "Your gmail.com or google account password WILL NOT WORK. "
        "Use one of following options to generate dedicated password for "
        "your Misago site to use when sending e-mails:"
    )
    print()
    print(
        "If you have 2-Step Verification enabled:         "
        "https://security.google.com/settings/security/apppasswords"
    )
    print(
        "If you DON'T have 2-Step Verification enabled:   "
        "https://myaccount.google.com/lesssecureapps"
    )
    print()

    password_prompt = "Enter your Gmail application password: "
    password = None

    while not password:
        password = input(password_prompt).strip()
        if not password:
            password = None
            print("You have to enter a password.")
            print()

    email_from_prompt = 'Enter your sender name (eg. "Misago Forums", optional): '
    email_from = input(email_from_prompt).strip()

    env_file["MISAGO_EMAIL_PROVIDER"] = PROVIDER_GMAIL
    env_file["MISAGO_GMAIL_USER"] = email_address
    env_file["MISAGO_GMAIL_PASSWORD"] = password

    if email_from:
        env_file["MISAGO_DEFAULT_FROM_EMAIL"] = "%s <%s>" % (email_from, email_address)
    else:
        env_file["MISAGO_DEFAULT_FROM_EMAIL"] = email_address


def run_mailjet_wizard(env_file):
    api_key_prompt = "Enter your Mailjet API key: "
    api_key = None

    while not api_key:
        api_key = input(api_key_prompt).strip()
        if not api_key:
            api_key = None
            print("You have to enter an API key.")
            print()

    api_secret_prompt = "Enter your Mailjet secret key: "
    api_secret = None

    while not api_secret:
        api_secret = input(api_secret_prompt).strip()
        if not api_secret:
            api_secret = None
            print("You have to enter an secret key.")
            print()

    env_file["MISAGO_EMAIL_PROVIDER"] = PROVIDER_MAILJET
    env_file["MISAGO_MAILJET_API_KEY_PUBLIC"] = api_key
    env_file["MISAGO_MAILJET_API_KEY_PRIVATE"] = api_secret
    env_file["MISAGO_DEFAULT_FROM_EMAIL"] = ""


def run_sendinblue_wizard(env_file):
    api_key_prompt = "Enter your SendinBlue API key: "
    api_key = None

    while not api_key:
        api_key = input(api_key_prompt).strip()
        if not api_key:
            api_key = None
            print("You have to enter an API key.")
            print()

    env_file["MISAGO_EMAIL_PROVIDER"] = PROVIDER_SENDINBLUE
    env_file["MISAGO_SENDINBLUE_API_KEY"] = api_key
    env_file["MISAGO_DEFAULT_FROM_EMAIL"] = ""


def print_email_setup(env_file):
    if env_file.get("MISAGO_EMAIL_PROVIDER") == PROVIDER_CONSOLE:
        print("Sending e-mails is currently disabled.")

    if env_file.get("MISAGO_EMAIL_PROVIDER") == PROVIDER_SMTP:
        print_smtp_setup(env_file)

    if env_file.get("MISAGO_EMAIL_PROVIDER") == PROVIDER_GMAIL:
        print_gmail_setup(env_file)

    if env_file.get("MISAGO_EMAIL_PROVIDER") == PROVIDER_MAILJET:
        print_mailjet_setup(env_file)

    if env_file.get("MISAGO_EMAIL_PROVIDER") == PROVIDER_SENDINBLUE:
        print_sendinblue_setup(env_file)


def print_smtp_setup(env_file):
    print("Using custom SMTP configuration to send e-mails:")
    print()
    print("From:        %s" % env_file.get("MISAGO_DEFAULT_FROM_EMAIL"))
    print("User:        %s" % env_file.get("MISAGO_EMAIL_USER", ""))
    print("Password:    %s" % env_file.get("MISAGO_EMAIL_PASSWORD", ""))
    print("Host:        %s" % env_file.get("MISAGO_EMAIL_HOST", ""))
    print("Port:        %s" % env_file.get("MISAGO_EMAIL_PORT", ""))
    print("SSL:         %s" % get_bool_display(env_file.get("MISAGO_EMAIL_USE_SSL")))
    print("TLS:         %s" % get_bool_display(env_file.get("MISAGO_EMAIL_USE_TLS")))


def print_gmail_setup(env_file):
    print("Using Gmail to send e-mails:")
    print()
    print("From:        %s" % env_file.get("MISAGO_DEFAULT_FROM_EMAIL"))
    print("User:        %s" % env_file.get("MISAGO_GMAIL_USER", ""))
    print("Password:    %s" % env_file.get("MISAGO_GMAIL_PASSWORD", ""))


def print_mailjet_setup(env_file):
    print("Using Mailjet to send e-mails:")
    print()
    print("API key:     %s" % env_file.get("MISAGO_MAILJET_API_KEY_PUBLIC"))
    print("Secret key:  %s" % env_file.get("MISAGO_MAILJET_API_KEY_PRIVATE"))


def print_sendinblue_setup(env_file):
    print("Using SendinBlue to send e-mails:")
    print()
    print("API key:     %s" % env_file.get("MISAGO_SENDINBLUE_API_KEY"))


def change_email_setup(env_file):
    print_email_setup(misago)
    print()
    if input_bool("Change e-mail configuration?", default=False):
        run_email_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_email_setup(misago)
        except KeyboardInterrupt:
            print()
