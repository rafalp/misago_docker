Misago Docker
=============

⚠️ **WARNING: This repository is work in progress, don't use it yet!** ⚠️

This repository aims to provide black-box production-quality setup of Misago for people who:

- Want to run their own forum using Misago
- Have a server with Docker lying around
- Know enough of Linux to ssh to VPS, move around, modify files, run programs and follow instructions from guides

**Note for DevOps pros:** this repo assumes that users will `git clone` it on to their servers, run `./appctl setup` to do basic configuration, and run all services they need in Docker Compose, with all data stored on instance using Docker volumes. This approach is incompatibile with setups where everything runs in dedicated instance or service (like Amazon's S3 or RDS), but the aim of this repo is to make Misago viable option to hobbyists and small/medium communities, not enterprise deployments that will expect running at massive scale serving bazillions of active users at single time.


Getting started
---------------

To start your own Misago site, you will need:

- server running Linux with Dockerm with at least 2GB of memory ([DigitalOcean droplets are safe bet.](https://m.do.co/c/a8c85735320a))
- domain your site will run at, directed to your server


⚠️ This section will be filled in at later time.


### Speed up Redis

Misago uses Redis for caching and tasks queue. To get most performance out of it, you will have to make sure that you have `Transparent Huge Pages (THP)` support disabled in your kernel. To fix this issue run the command `echo never > /sys/kernel/mm/transparent_hugepage/enabled` as root, and add it to your `/etc/rc.local` in order to retain the setting after a reboot. Docker Redis container must be restarted after THP is disabled, but you can simply run `./appctl restart` for same effect.

This is impossible if you are running Misago on macOS.


### Secure your server

Depending on initial configuration of your server, you may have to take [additional steps](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) to make it more secure. Internet is patrolled by bots searching for vulnerable servers, not above attempting to brute-force root accounts, so you should at least disable the login using root, and block IP addresses upon repeated failed authentication attempts.


### Enable Sentry

You can also create account on Sentry (https://sentry.io) and enable it on your side using `./appctl sentry` so you will receive e-mail notifications when your users experience errors or edit their profile details, which is possible source of forum spam.


Customizing site
----------------

⚠️ This section will be filled in at later time.


Backup and restore
------------------

### Creating new backup

Running the `./appctl backup` will result in new backup being created in `backups` directory, under the path corresponding to year and month of backup's creation (eg. 2018/10 for backups created in october 2018).

Backup will be a `tar.gz` archive named using `misago-YYYYMMDDHHMMSS.tar.gz` format and will contain `database.sql` file with database export created using `pg_dump`, and `media` directory contained user-uploaded files.


### Restoring from backup

You can restore your site's data by placing the backup archive in the `backups` directory, and running `./appctl restore yourbackupfile.tar.gz`. If your backup file is located in the subdirectory, you can specify the path to it relative to `backups`, eg.: `./appctl restore 2018/10/yourbackupfile.tar.gz`.

Restoration will:

- overwrite your current `media` directory with one from archive.
- load the `database.sql` to `psql`, overwriting existing database tables with ones from file.

**NOTE:** because restoration process can be considered descructive, you should backup any existing data if you are restoring the site that has data you may want to recover if something goes wrong.

After you've restored from backup, it's good idea to follow up with `./appctl rebuild` to rebuild Misago image, giving it's application container a chance to rebuild filesystem caches.


### Daily backup

`./appctl setup` enables daily backup by default. This backup is defined in `cron` script inside Misago container, and is ran *before* all other maintenance tasks, providing fallback point in case that maintenance deletes something you **really** didn't want to delete.

You can switch daily backup on and off using `./appctl dailybackup`.


Directories
-----------

### `/backups`

Contains backups created by `./appctl backup` and loadable by `./appctl restore BACKUPNAME`.


### `/env`

This directory contains configuration for Misago and PostgreSQL containers.


### `/logs`

Log files created by Misago container. If you are experiencing errors, see `misago.log` or `uwsgi.log` file contents for complete error message together with backtrace.


### `/misago`

Defines docker container for Misago complete with UWSGI server running Misago and serving its static files.


### `/wizard`

Python scripts that `./appctl` runs when it needs to create or change `.env` files with configuration.


Need help?
----------

If you have problems setting up your site using `Misago-Docker`, feel free to ask on [our forums](https://misago-project.org/) or [Discord Chat](https://discord.gg/fwvrZgB). Please don't use Github issues!


Contributing
------------

If you found a bug, issue, or place for improvement, feel free to open an issue or pull request.


Copyright and license
---------------------

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.
