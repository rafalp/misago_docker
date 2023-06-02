from config import misago
from misago import run_misago_wizard

WIZARDS_ANDS_FILES = ((run_misago_wizard, misago),)

if __name__ == "__main__":
    try:
        run_misago_wizard(misago)
    except KeyboardInterrupt:
        print()
