import os

from envfile import EnvFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "env")

misago = EnvFile(os.path.join(ENV_DIR, "misago.env"))
postgres = EnvFile(os.path.join(ENV_DIR, "postgres.env"))
