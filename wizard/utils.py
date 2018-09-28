import random


def ask_for_bool(question, default=True):
    if default:
        suggestion = "Y/n"
    else:
        suggestion = "N/y"
    print("%s (%s):" % (question, suggestion))


RANDOM_CHARS = (
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)


def get_random_string(length, allowed_chars=RANDOM_CHARS):
    return ''.join(random.choice(allowed_chars) for i in range(length))


def get_random_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)