Misago Docker
=============

This repository provides production-ready setup of Misago for people who:

- Want to run their own forum using Misago
- Have a server with 2GB of RAM and Docker lying around
- Know enough of Linux to ssh to VPS, move around, modify files, run programs and follow instructions from guides

It provides Misago forum running on Python 3.7 behind Nginx reverse proxy with Https enabled via Let's Encrypt, PostgreSQL database and Redis for caching.

To help you running your site, there is a special tool called `appctl` provided, that consists of shortcuts for useful actions, and exposes wizards for configuration management without the need for manually editing files.

**Note for DevOps pros:** this repo assumes that users will `git clone` it on to their servers, run `./appctl setup` to do basic configuration, and run all services they need in Docker Compose, with all data stored on instance using Docker volumes. This approach is incompatibile with setups where everything runs in dedicated instance or service (like Amazon's S3 or RDS), but the aim of this repo is to make Misago viable option to hobbyists and small/medium communities, not enterprise deployments that will expect running at massive scale serving bazillions of active users at single time.


Setup
-----

For complete step-by-step setup guide, please see [the documentation](https://misago.gitbook.io/docs/setup).

To start your own Misago site, you will need:

- server running Linux with Docker and 2GB of memory ([DigitalOcean droplets are safe bet](https://m.do.co/c/a8c85735320a))
- domain your site will run at, configured to point at your server


### Getting code on the server

`ssh` to your server. If you are on Windows, you can use [Putty](https://www.putty.org/). Next, git clone this repo to using this command:

```
git clone https://github.com/rafalp/misago_docker.git --depth=1
```

This will create `misago_docker` directory that you can then `cd` to and continue site setup.


### Running the setup

Enter the misago_docker directory and run `./appctl setup` command. The wizard will let you set basic settings for your site: your domain name, timezone or first admin account details. After that it will:

- install all requirements
- build Docker containers
- setup `crontab` that will run daily maintenance
- create database and populate it with initial data

When `setup` finishes, visit your domain in order to see your Misago forum running.

Lastly, go to `https://yourdomain.com/admincp/` and log into the admin panel using the username and password you entered during the setup. There you will be able to further configure your forum. For instance: set forum name, create categories and such.


### Secure your server

Depending on initial configuration of your server, you may have to take [additional steps](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) to make it more secure. Internet is patrolled by bots searching for vulnerable servers attempting to brute-force root accounts so you should disable the root login, block IP addresses upon repeated failed authentication attempts, or both. You can easilly enable 10-minute ban for 3 failed sign-in entries by installing `fail2ban`:

```
apt-get install fail2ban
```


### Setup e-mail

If you haven't done so during installation, you *really* should enable e-mails on your site. Not enabling e-mails doesn't mean that Misago will fallback to some other messaging mechanism. It will simply discard all messages without attempting to connect to any e-mail sending service.

Without e-mails enabled your users will not be able to receive activation e-mails, notifications, confirm password changes or reset forgotten passwords.


### Enable Sentry

You can also create account on Sentry (https://sentry.io) and enable it on your site using `./appctl sentry`. Sentry provides fancy web interface for browsing Misago's logs, and will send you e-mail with notifications when your users experience errors or edit their profile details, which is possible source of forum spam.


### Speed up Redis

Misago uses Redis for caching and tasks queue. To get most performance out of it, you will have to make sure that you have `Transparent Huge Pages (THP)` support disabled in your kernel. To do that run the command `echo never > /sys/kernel/mm/transparent_hugepage/enabled` as root, and add it to your `/etc/rc.local` in order to retain the setting after a reboot. Docker Redis container must be restarted after THP is disabled, but you can simply run `./appctl restart` for same effect.


Upgrading to newer version
--------------------------

To upgrade to newer version, go to `misago_docker` directory and run `./apctl upgrade`. This will backup your data, get latest code from github, rebuild Docker containers and update Misago (and other services) to latest minor releases.

You may have to setup git credentials on your machine for `git pull` to work, but entering git password is not required.


Backup and restore
------------------

### Creating new backup

Running the `./appctl backup` will result in new backup being created in `backups` directory.

Backup will be a `tar.gz` archive named following the `manual-YYYYMMDDHHMMSS.tar.gz` format and will contain `database.sql` file with database export created using `pg_dump`, and `media` directory containing user-uploaded files.


### Restoring from backup

You can restore your site's data by placing the backup archive in the `backups` directory, and running `./appctl restore yourbackupfile.tar.gz`. If your backup file is located in the subdirectory, you can specify the path to it relative to `backups`, eg.: `./appctl restore 2018/10/yourbackupfile.tar.gz`.

Restoration will:

- overwrite your current `media` directory with one from archive.
- load the `database.sql` to `psql`, overwriting existing database tables with ones from file.

**NOTE:** because restoration process can be considered destructive, you should backup existing data if you are restoring the site that has any data you may want to recover if something goes wrong.

After you've restored from backup, it's good idea to follow up with `./appctl rebuild` to rebuild Misago image, giving it's application container a chance to rebuild filesystem caches.


### Daily backup

`./appctl` adds daily backup to system cron. This backup is ran *before* all other maintenance tasks, providing fallback point in case that maintenance deletes something you **really** didn't want to delete. Automatic backup files start with `auto-` and are deleted automatically after 10 days.


### Creating custom backup archives

You can create your own backup archives for use with `./appctl restore`.

Start off with creating a directory, `mybackup` for instance. Create the following files and directories inside of it:

`database.sql` - PostgreSQL dump that can be imported with `psql`.
`media` - your forum's media directory.

Your ready backup should look like this:

```
mybackup
  - media
  - database.sql
```

Now run `tar -zcf mybackup.tar.gz mybackup`. This will produce the `mybackup.tar.gz` file that you can put in `backups` directory and restore with `./appctl restore mybackup.tar.gz`. 


Customizing site
----------------

Inside `misago/theme` directory you will find two folders that allow you to customise your site's looks:

`static` for overriding/adding static files such as css, js, images or fonts.
`templates` for overriding Django templates with custom ones.


### Example: Replacing Misago's css with custom one

> You may want to use *themes* feature available in admin control panel instead.

Let's say you've cloned [main repo](https://github.com/rafalp/Misago) to your dev machine. Got it running and customised the CSS to make your site's theme dark instead of default. You've ran build script and got final `misago.css` file containing your changes. How do you now deploy this file to production?

First, you need to find out the path of the original file relative to its `static` directory. In case of Misago this is `static/misago/css/misago.css`. This means that to make Misago use your file instead of default, it should be deployed to `theme/static/misago/css/misago.css` original.

After deploying your new file, run `./appctl collectstatic` to make Misago "collect" this file and replace default with it.


### Sticking a fork into the repo

If you are familiar with Python/Django applications or Docker images involved and wish to customise your setup further, please feel free to branch off/fork the repo - it's simple enough that merging eventual changes from upstream shouldn't be much of an issue.


Overriding configuration
------------------------

To override configuration in `docker-compose.yml`, create `docker-compose.override.yml` file next to it, and re-define selected parts in it. For example, to change default HTTP for NGINX proxy from 80 to 8080, you can include following configuration in your override:

```yml
version: '3.0'
services:

  nginx-proxy:
    ports:
      - "8080:80"
```

To add or change settings defined in `settings.py` that don't support change via environment variable, you can create additional file `settings_override.py` next to it:

```python
SESSION_COOKIE_NAME = "myforumsid"
```

To add custom urls to the site, create `urls_override.py` file that contains custom `urlpatterns`:

```python
from django.conf.urls import include

urlpatterns = [
    url(r"^my-app/", include("myapp.urls")),
]
```

Because `urlpatterns` defined in override are checked before default ones, this approach supports overriding already-existing urls.


Directories
-----------

### `/backups`

Contains backups created by `./appctl backup` and loadable by `./appctl restore BACKUPNAME`.


### `/config`

This directory contains configuration for Misago and PostgreSQL containers as well as Nginx config.


### `/logs`

Log files created by Misago container. If you are experiencing errors, see `misago.log` or `uwsgi.log` file contents for complete error message together with backtrace.


### `/misago`

Defines Docker container for Misago complete with UWSGI server running Misago and serving its static files.


### `/nginx-proxy`

Extends [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) Docker image to disable TLSv1.0 https encryption on your site, improving it's security rating.


### `/wizard`

Python scripts that `./appctl` runs when it needs to create or change `.env` files with configuration.


Conserving disk space
---------------------

Docker overhead on CPU and memory is negligible, but same can't be said about its disk usage. `./appctl` tries to cleanup whenever possible, but to be safe you will have to monitor amount of free space left on your server, and clean up once in a while using commands like `docker-compose image prune`, manually emptying older logs and backups stored in `logs` and `backups` directories.

Default cron task will also try to delete log files older than 60 days.


Need help?
----------

If you have problems setting up your site using `misago_docker`, feel free to ask on [our forums](https://misago-project.org/) or [Discord Chat](https://discord.gg/fwvrZgB). Please don't use Github issues!


Contributing
------------

If you've found a bug, issue, or place for improvement, please open an issue or pull request.


Copyright and license
---------------------

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.
