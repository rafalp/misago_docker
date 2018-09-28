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

    print("Generated postgres.env file with following database settings:")
    print()
    print("User:       %s" % env_file["POSTGRES_USER"])
    print("Password:   %s" % env_file["POSTGRES_PASSWORD"])


def update_postgres_env_file(env_file):
    save_changes = False

    print("postgres.env already exists, updating entries:")
    print()

    if not env_file.get("POSTGRES_USER"):
        env_file["POSTGRES_USER"] = "misago%s" % get_random_string(16)
        save_changes = True
        
        print("User:       %s" % env_file["POSTGRES_USER"])

    if not env_file.get("POSTGRES_PASSWORD"):
        env_file["POSTGRES_PASSWORD"] = "%s" % get_random_string(100)
        save_changes = True
        
        print("Password:   %s" % env_file["POSTGRES_PASSWORD"])
        
    if save_changes:
        print()
        print("postgres.env has been updated!")
        env_file.save(FILE_HEADER)
    else:
        print("Already up to date!")
