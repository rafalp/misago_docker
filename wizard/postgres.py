from utils import get_random_string

FILE_HEADER = "PostgreSQL service settings"


def run_postgres_wizard(env_file):
    if env_file.is_file():
        update_postgres_env_file(env_file)
    else:
        generate_default_postgres_env_file(env_file)


def generate_default_postgres_env_file(env_file):
    env_file["POSTGRES_USER"] = "misago%s" % get_random_string(16)
    env_file["POSTGRES_PASSWORD"] = "%s" % get_random_string(100)
    env_file.save(FILE_HEADER)

    print("PostgreSQL configuration has been saved to %s" % env_file.path)


def update_postgres_env_file(env_file):
    changes = []

    if not env_file.get("POSTGRES_USER"):
        env_file["POSTGRES_USER"] = "misago%s" % get_random_string(16)
        changes.append("User:       %s" % env_file["POSTGRES_USER"])

    if not env_file.get("POSTGRES_PASSWORD"):
        env_file["POSTGRES_PASSWORD"] = "%s" % get_random_string(100)
        changes.append("Password:   %s" % env_file["POSTGRES_PASSWORD"])

    if changes:
        print(
            "PostgreSQL configuration file has been updated with following database settings:"
        )
        print()
        print("\n".join(changes))
        env_file.save(FILE_HEADER)
    else:
        print("PostgreSQL configuration file is up to date.")
