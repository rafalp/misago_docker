import filecmp
import os
from pathlib import Path
from shutil import copy

from config import CERTS_DIR, VHOSTD_DIR
from utils import input_bool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VHOST_LOCATION_CONFIG = os.path.join(BASE_DIR, "nginx", "vhost_location")


def run_nginx_wizard(hostname):
    create_nginx_vhostd_if_not_exists()
    create_nginx_certs_if_not_exists()
    return create_nginx_location_config(hostname)


def create_nginx_vhostd_if_not_exists():
    ngnix_vhostd_path = Path(VHOSTD_DIR)
    if not ngnix_vhostd_path.exists():
        ngnix_vhostd_path.mkdir()


def create_nginx_certs_if_not_exists():
    ngnix_certs_path = Path(CERTS_DIR)
    if not ngnix_certs_path.exists():
        ngnix_certs_path.mkdir()


def create_nginx_location_config(hostname):
    config_filename = "%s_location" % hostname
    config_dst = Path(os.path.join(VHOSTD_DIR, config_filename))
    if config_dst.is_file():
        if filecmp.cmp(VHOST_LOCATION_CONFIG, config_dst):
            # Skip rest of wizard because destination file already exists
            return True

        overwrite_prompt = (
            "config/vhost.d/%s already exists but appears to be modified, overwrite with default?"
        ) % config_filename
        if not input_bool(overwrite_prompt, default=False):
            return False
        config_dst.unlink()
    copy(VHOST_LOCATION_CONFIG, config_dst)
    return True
