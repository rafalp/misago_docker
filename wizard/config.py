import os

from envfile import EnvFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
VHOSTD_DIR = os.path.join(CONFIG_DIR, "vhost.d")

MISAGO_HEADER = "Misago service settings"
misago = EnvFile(MISAGO_HEADER, os.path.join(CONFIG_DIR, "misago.env"))

POSTGRES_HEADER = "PostgreSQL database settings"
postgres = EnvFile(POSTGRES_HEADER, os.path.join(CONFIG_DIR, "postgres.env"))
