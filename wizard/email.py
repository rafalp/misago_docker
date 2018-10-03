from utils import input_bool, input_choice


def run_email_wizard(env_file):
    email_provider_prompt = [
        "Which e-mail provider do you want to use?",
        "",
        "0 - None (disables sending e-mails)",
        "1 - SMTP",
        "2 - Gmail (gmail.com)",
        "3 - Mailgun (mailgun.com)",
        "4 - Mailjet (mailjet.com)",
        "5 - SendinBlue (sendinblue.com/)",
        "",
        "Enter choice's number",
    ]

    email_provider = input_choice("\n".join(email_provider_prompt), "012345")

    wizards_map = {
        0: disable_sending_emails,
        1: run_smtp_wizard,
        2: run_gmail_wizard,
        3: run_mailgun_wizard,
        4: run_mailjet_wizard,
        5: run_sendinblue_wizard,
    }

    email_provider_wizard = wizards_map[int(email_provider)]
    email_provider_wizard(env_file)


def disable_sending_emails(env_file):
    env_file["MISAGO_EMAIL_PROVIDER"] = "console"


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

    env_file["MISAGO_EMAIL_PROVIDER"] = "smtp"
    env_file["MISAGO_EMAIL_HOST"] = email_host
    env_file["MISAGO_EMAIL_USER"] = email_user
    env_file["MISAGO_EMAIL_PASSWORD"] = email_password
    env_file["MISAGO_EMAIL_USE_SSL"] = "yes" if email_ssl else "no"
    env_file["MISAGO_EMAIL_USE_TLS"] = "yes" if email_tls else "no"
    env_file["MISAGO_EMAIL_PORT"] = email_port

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

    env_file["MISAGO_EMAIL_PROVIDER"] = "gmail"
    env_file["MISAGO_GMAIL_USER"] = email_address
    env_file["MISAGO_GMAIL_PASSWORD"] = password

    if email_from:
        env_file["MISAGO_DEFAULT_FROM_EMAIL"] = "%s <%s>" % (email_from, email_address)
    else:
        env_file["MISAGO_DEFAULT_FROM_EMAIL"] = email_address


def run_mailgun_wizard(env_file):
    api_key_prompt = "Enter your Mailgun api key: "
    api_key = None

    while not api_key:
        api_key = input(api_key_prompt).strip()
        if not api_key:
            api_key = None
            print("You have to enter an api key.")
            print()

    env_file["MISAGO_EMAIL_PROVIDER"] = "mailgun"
    env_file["MISAGO_MAILGUN_API_KEY"] = api_key
    env_file["MISAGO_DEFAULT_FROM_EMAIL"] = ""


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

    env_file["MISAGO_EMAIL_PROVIDER"] = "mailjet"
    env_file["MISAGO_MAILJET_API_KEY_PUBLIC"] = api_key
    env_file["MISAGO_MAILJET_API_KEY_PRIVATE"] = api_secret
    env_file["MISAGO_DEFAULT_FROM_EMAIL"] = ""


def run_sendinblue_wizard(env_file):
    api_key_prompt = "Enter your SendinBlue api key: "
    api_key = None

    while not api_key:
        api_key = input(api_key_prompt).strip()
        if not api_key:
            api_key = None
            print("You have to enter an api key.")
            print()

    env_file["MISAGO_EMAIL_PROVIDER"] = "sendinblue"
    env_file["MISAGO_SENDINBLUE_API_KEY"] = api_key
    env_file["MISAGO_DEFAULT_FROM_EMAIL"] = ""
