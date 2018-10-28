from email import run_email_wizard
from hostname import run_hostname_wizard
from locale import run_locale_wizard
from secretkey import set_random_secret_key
from timezone import run_timezone_wizard


def run_misago_wizard(env_file):
    # Disable debug by default, because it's safer that way
    env_file["MISAGO_DEBUG"] = "no"

    # Enable daily backup, just to be safe
    env_file["MISAGO_DAILY_BACKUP"] = "yes"

    # Generate random secret key using Django's algorithm
    set_random_secret_key(env_file)

    # Ask user to fill in some values
    run_hostname_wizard(env_file)
    run_locale_wizard(env_file)
    run_timezone_wizard(env_file)
    run_email_wizard(env_file)

    env_file.save()
    print("Misago configuration has been saved to %s" % env_file.path)
