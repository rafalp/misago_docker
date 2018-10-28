from utils import get_random_string


def run_postgres_wizard(env_file):
    if env_file.is_file():
        update_postgres_env_file(env_file)
    else:
        generate_default_postgres_env_file(env_file)


def generate_default_postgres_env_file(env_file):
    env_file["POSTGRES_USER"] = "misago_%s" % get_random_string(16)
    env_file["POSTGRES_PASSWORD"] = "%s" % get_random_string(80)
    env_file.save()

    print("PostgreSQL configuration has been saved to %s" % env_file.path)


def update_postgres_env_file(env_file):
    changes = []

    if not env_file.get("POSTGRES_USER"):
        env_file["POSTGRES_USER"] = "misago_%s" % get_random_string(16)
        changes.append("User:       %s" % env_file["POSTGRES_USER"])

    if not env_file.get("POSTGRES_PASSWORD"):
        env_file["POSTGRES_PASSWORD"] = "%s" % get_random_string(80)
        changes.append("Password:   %s" % env_file["POSTGRES_PASSWORD"])

    if changes:
        env_file.save()
        print(
            "PostgreSQL configuration file has been updated with following database settings:"
        )
        print()
        print("\n".join(changes))
    else:
        print("PostgreSQL configuration file is up to date.")
