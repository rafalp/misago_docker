import os

from envfile import EnvFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
NGINX_DIR = os.path.join(CONFIG_DIR, "vhost.d")

misago = EnvFile(os.path.join(CONFIG_DIR, "misago.env"))
postgres = EnvFile(os.path.join(CONFIG_DIR, "postgres.env"))
