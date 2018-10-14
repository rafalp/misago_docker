from env import misago
from utils import input_bool, print_setup_changed_message, serialize_bool

BOOL_TRUE = "yes"  # we are specific here because bash script bool check if simple


def print_daily_backup_setup(env_file):
    if env_file.get("MISAGO_DAILY_BACKUP", "").lower() == BOOL_TRUE:
        print("Automatic daily backup is enabled.")
    else:
        print("Automatic daily backup is disabled.")


def change_daily_backup_setup(env_file):
    print_daily_backup_setup(misago)
    print()

    daily_backup_is_enabled = (
        env_file.get("MISAGO_DAILY_BACKUP", "").lower() == BOOL_TRUE
    )
    if daily_backup_is_enabled:
        backup_prompt = "Disable automatic daily backup?"
    else:
        backup_prompt = "Enable automatic daily backup?"

    if input_bool(backup_prompt, default=not daily_backup_is_enabled):
        new_daily_backup_mode = (
            env_file.get("MISAGO_DAILY_BACKUP", "").lower() != BOOL_TRUE
        )
        env_file["MISAGO_DAILY_BACKUP"] = serialize_bool(new_daily_backup_mode)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_daily_backup_setup(misago)
        except KeyboardInterrupt:
            print()
