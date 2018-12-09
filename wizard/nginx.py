import filecmp
import os
from pathlib import Path

from config import VHOSTD_DIR
from utils import input_bool, save_cmp, safe_copy, safe_open

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VHOST_LOCATION_CONFIG = os.path.join(BASE_DIR, "nginx", "vhost_location")
REDIRECT_CONFIG = os.path.join(BASE_DIR, "nginx", "redirect")


def run_nginx_wizard(env_file):
    create_nginx_vhostd_if_not_exists()
    hostname = env_file["VIRTUAL_HOST"].split(",")[0]
    config_set = create_nginx_location_config(hostname)
    if config_set:
        clear_old_nginx_config(hostname)
        redirect_set = create_nginx_redirect_config(env_file, hostname)
    return config_set or redirect_set


def create_nginx_vhostd_if_not_exists():
    ngnix_vhostd_path = Path(VHOSTD_DIR)
    if not ngnix_vhostd_path.exists():
        ngnix_vhostd_path.mkdir()


def create_nginx_location_config(hostname):
    config_filename = "%s_location" % hostname
    config_dst = Path(os.path.join(VHOSTD_DIR, config_filename))
    if config_dst.is_file():
        if save_cmp(VHOST_LOCATION_CONFIG, config_dst):
            # Skip rest of wizard because destination file already exists
            return True

        overwrite_prompt = (
            "config/vhost.d/%s already exists but appears to be modified, "
            "overwrite with default?"
        ) % config_filename
        if not input_bool(overwrite_prompt, default=False):
            return False
        config_dst.unlink()

    safe_copy(VHOST_LOCATION_CONFIG, config_dst)
    return True


def clear_old_nginx_config(hostname):
    if hostname.startswith("www."):
        redirect_from = hostname[4:]
    else:
        redirect_from = "www.%s" % hostname

    old_redirect = Path(os.path.join(VHOSTD_DIR, hostname))
    if old_redirect.is_file():
        old_redirect.unlink()

    old_location_filename = "%s_location" % redirect_from
    old_location = Path(os.path.join(VHOSTD_DIR, old_location_filename))
    if old_location.is_file():
        old_location.unlink()


def create_nginx_redirect_config(env_file, hostname):
    if hostname.startswith("www."):
        redirect_from = hostname[4:]
    else:
        redirect_from = "www.%s" % hostname

    config_dst = Path(os.path.join(VHOSTD_DIR, redirect_from))

    redirect_prompt = (
        "Do you want to set 301 redirect from %s to %s? "
        "(requires domain to be already configured)"
    ) % (redirect_from, hostname)
    if input_bool(redirect_prompt):
        env_file["LETSENCRYPT_HOST"] = env_file["VIRTUAL_HOST"]
        env_file.save()
    else:
        env_file["LETSENCRYPT_HOST"] = hostname
        env_file.save()
        if config_dst.is_file():
            config_dst.unlink()
        return False

    with safe_open(REDIRECT_CONFIG, "r") as f:
        tpl = f.read()
    redirect_config = tpl.replace("domain.com", hostname)

    with safe_open(config_dst, "w") as f:
        f.write(redirect_config)

    return True
