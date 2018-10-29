import filecmp
import os
from pathlib import Path
from shutil import copy

from config import VHOSTD_DIR
from utils import input_bool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VHOST_LOCATION_CONFIG = os.path.join(BASE_DIR, "nginx", "vhost_location")
REDIRECT_CONFIG = os.path.join(BASE_DIR, "nginx", "redirect")


def run_nginx_wizard(hostname):
    create_nginx_vhostd_if_not_exists()
    config_set = create_nginx_location_config(hostname)
    redirect_set = create_nginx_redirect_config(hostname)
    return config_set or redirect_set


def create_nginx_vhostd_if_not_exists():
    ngnix_vhostd_path = Path(VHOSTD_DIR)
    if not ngnix_vhostd_path.exists():
        ngnix_vhostd_path.mkdir()


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


def create_nginx_redirect_config(hostname):
    if hostname.startswith("www."):
        redirect_from = hostname[4:]
    else:
        redirect_from = "www.%s" % hostname

    config_dst = Path(os.path.join(VHOSTD_DIR, redirect_from))
    if config_dst.is_file():
        overwrite_prompt = (
            "config/vhost.d/%s already exists, overwrite with new one?"
        ) % redirect_from
        if not input_bool(overwrite_prompt, default=False):
            return False

    with open(REDIRECT_CONFIG, "r") as f:
        tpl = f.read()
    redirect_config = tpl.replace("domain.com", hostname)

    with open(config_dst, "w") as f:
        f.write(redirect_config)

    return True
