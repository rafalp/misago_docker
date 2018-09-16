"""
Utility functions for reading configuration from env variables.
"""
import os

BOOL_TRUE = ('y', 'yes', 'true', '1')


def get_bool(name, default=False):
    if name not in os.environ:
        return default
    return os.environ[name].lower() in BOOL_TRUE


def get_list(name, default=None):
    if name not in os.environ:
        return default or []
    return [item.strip() for item in os.environ.get(name).split(',')]