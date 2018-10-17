from config import misago, postgres
from misago import run_misago_wizard
from postgres import run_postgres_wizard

WIZARDS_ANDS_FILES = ((run_misago_wizard, misago), (run_postgres_wizard, postgres))

if __name__ == "__main__":
    try:
        for run_wizard, env_file in WIZARDS_ANDS_FILES:
            run_wizard(env_file)
    except KeyboardInterrupt:
        print()
