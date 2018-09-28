from utils import get_random_secret_key

FILE_HEADER = "Misago service settings"


def run_misago_wizard(env_file):
    env_file["DEBUG"] = "no"
    env_file["VIRTUAL_HOST"] = "misagosite.com"
    env_file["SECRET_KEY"] = get_random_secret_key()
    env_file["LANGUAGE_CODE"] = "en"
    env_file["TIME_ZONE"] = "utc"
    env_file["SEARCH_CONFIG"] = "simple"
    env_file["DEFAULT_FROM_EMAIL"] = "fixme"
    env_file["MAILGUN_API_KEY"] = "fixme"
    env_file["MAILJET_API_KEY_PUBLIC"] = "fixme"
    env_file["MAILJET_API_KEY_PRIVATE"] = "fixme"
    env_file["SENDINBLUE_API_KEY"] = "fixme"
    env_file["SENTRY_DSN"] = "fixme"

    env_file.save(FILE_HEADER)
