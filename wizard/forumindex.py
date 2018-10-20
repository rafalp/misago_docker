from config import misago
from utils import BOOL_TRUE, input_bool, input_choice, print_setup_changed_message


def run_forum_index_wizard(env_file):
    forum_index_prompt = [
        "What content do you want to display on forum index?",
        "",
        "1 - Threads",
        "2 - Categories",
        "",
        "Enter choice's number",
    ]

    forum_index = input_choice("\n".join(forum_index_prompt), "12", coerce_to=int)

    choices_values = {1: "threads", 2: "categories"}

    env_file["MISAGO_INDEX"] = choices_values[forum_index]


def print_forum_index_setup(env_file):
    if env_file.get("MISAGO_INDEX", "threads") == "threads":
        print("Forum index is showing threads list.")
    else:
        print("Forum index is showing categories list.")


def change_forum_index_setup(env_file):
    print_forum_index_setup(misago)
    print()
    if input_bool("Change forum index?", default=False):
        run_forum_index_wizard(env_file)
        env_file.save()
        print_setup_changed_message()


if __name__ == "__main__":
    if misago.is_file():
        try:
            change_forum_index_setup(misago)
        except KeyboardInterrupt:
            print()
