"""
Utility functions for reading configuration from env variables.
"""
import os

BOOL_TRUE = ('y', 'yes', 'true', '1')


def strtobool(value):
    if value is None:
        return False
    return value.lower() in BOOL_TRUE


def strtolist(value):
    if value is None:
        return []
    return [item.strip() for item in value.split(',')]