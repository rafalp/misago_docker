
import os

from envfile import EnvFile
from misago import run_misago_wizard
from postgres import run_postgres_wizard

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, 'env')

WIZARDS_ANDS_FILES = (
    (run_misago_wizard, 'misago.env'),
    (run_postgres_wizard, 'postgres.env'),
)

if __name__ == "__main__":
    for run_wizard, filename in WIZARDS_ANDS_FILES:
        run_wizard(EnvFile(os.path.join(ENV_DIR, filename)))
        print()
