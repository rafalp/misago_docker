import os
from pathlib import Path
from shutil import copy

from config import NGINX_DIR
from utils import input_bool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VHOST_LOCATION_CONFIG = os.path.join(BASE_DIR, "nginx", "vhost_location")


def run_nginx_wizard(hostname):
    create_nginx_vhostd_if_not_exists()
    return create_nginx_location_config(hostname)


def create_nginx_vhostd_if_not_exists():
    ngnix_vhostd_path = Path(NGINX_DIR)
    if not ngnix_vhostd_path.exists():
        ngnix_vhostd_path.mkdir()


def create_nginx_location_config(hostname):
    config_filename = "%s_location" % hostname
    config_dst = Path(os.path.join(NGINX_DIR, config_filename))
    if config_dst.is_file():
        overwrite_prompt = (
            "config/vhost.d/%s already exist, overwrite it?"
        ) % config_filename
        if not input_bool(overwrite_prompt, default=False):
            return False
        config_dst.unlink()
    copy(VHOST_LOCATION_CONFIG, config_dst)
    return True
