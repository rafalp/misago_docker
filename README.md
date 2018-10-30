Misago Docker
=============

⚠️ **WARNING: This repository is work in progress, don't use it yet!** ⚠️

This repository provides production-ready setup of Misago for people who:

- Want to run their own forum using Misago
- Have a server with 2GB of RAM and Docker lying around
- Know enough of Linux to ssh to VPS, move around, modify files, run programs and follow instructions from guides

It provides Misago forum running on Python 3.6 behind Nginx reverse proxy with Https enabled via Let's Encrypt, PostgreSQL database and Redis for caching.

To help you running your site, there is a special tool called `appctl` provided, that consists of some shortcuts for useful actions, and exposes wizards for configuration management without the need for manually editing files.

**Note for DevOps pros:** this repo assumes that users will `git clone` it on to their servers, run `./appctl setup` to do basic configuration, and run all services they need in Docker Compose, with all data stored on instance using Docker volumes. This approach is incompatibile with setups where everything runs in dedicated instance or service (like Amazon's S3 or RDS), but the aim of this repo is to make Misago viable option to hobbyists and small/medium communities, not enterprise deployments that will expect running at massive scale serving bazillions of active users at single time.


Setup
-----

To start your own Misago site, you will need:

- server running Linux with Docker with at least 2GB of memory ([DigitalOcean droplets are safe bet](https://m.do.co/c/a8c85735320a))
- domain your site will run at, pointing to your server


### Getting code on the server

`ssh` to your server. If you are on Windows, you can use [Putty](https://www.putty.org/). Next, git clone this repo to `misago_docker` directory using this command:

```
git clone https://github.com/rafalp/misago_docker.git --depth=1
```

### Running the setup

Enter the misago_docker directory and run `./appctl setup` command. The wizard will ask for some basic information, such as your domain name, timezone or first admin account details. After that it will:

- install all requirements
- build Docker containers
- setup `crontab`
- create database and populate it with initial data

Once you are done, start the application by running `./appctl start` and visit your domain in order to see your Misago forum running.

Lastly, go to `https://yourdomain.com/admincp/` and log into the admin panel using the username and password you entered during the setup. There you will be able to further configure your forum. For instance: set forum name, create categories and such.


### Secure your server

Depending on initial configuration of your server, you may have to take [additional steps](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) to make it more secure. Internet is patrolled by bots searching for vulnerable servers, not above attempting to brute-force root accounts, so you should at least disable the login using root, and block IP addresses upon repeated failed authentication attempts.


### Setup e-mail

If you haven't done so during installation, you *really* should enable e-mails on your site. Not enabling e-mails doesn't mean that Misago will fallback to some other messaging mechanism. It will simply discard all messages without attempting to connect to any e-mail sending service.

Without e-mails enabled your users will not be able to receive activation e-mails, notifications, confirm password changes or reset forgotten passwords.


### Enable Sentry

You can also create account on Sentry (https://sentry.io) and enable it on your side using `./appctl sentry`. Sentry provides fancy web interface browsing Misago's logs, and will send e-mail with notifications when your users experience errors or edit their profile details, which is possible source of forum spam.


### Speed up Redis

Misago uses Redis for caching and tasks queue. To get most performance out of it, you will have to make sure that you have `Transparent Huge Pages (THP)` support disabled in your kernel. To fix this issue run the command `echo never > /sys/kernel/mm/transparent_hugepage/enabled` as root, and add it to your `/etc/rc.local` in order to retain the setting after a reboot. Docker Redis container must be restarted after THP is disabled, but you can simply run `./appctl restart` for same effect.


Upgrading to newer version
--------------------------

To upgrade to newer version, simply run `git pull` followed by `./apctl upgrade`. This will get latest code from github, rebuild Docker containers and update Misago (and other services) to latest minor releases.


Backup and restore
------------------

### Creating new backup

Running the `./appctl backup` will result in new backup being created in `backups` directory, under the path corresponding to year and month of backup's creation (eg. 2018/10 for backups created in October 2018).

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


### Creating custom backup archives

You can easily prepare your own backup archives for use with `./appctl restore`.

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


Customising site
----------------

Inside `misago/theme` directory you will find two folders that allow you to customise your site's looks:

`static` for overriding/adding static files such as css, js, images or fonts.
`templates` for overriding Django templates with custom ones.


### Example: Replacing Misago's css with custom one

Let's say you've cloned [main repo](https://github.com/rafalp/Misago) to your dev machine. Got it running and customised the CSS to make your site's theme dark instead of default. You've ran build script and got final `misago.css` file containing your changes. How do you now deploy this file to production?

First, you need to find out the path of the original file relative to its `static` directory. In case of Misago this is `static/misago/css/misago.css`. This means that to make Misago use your file instead of default, it should be deployed to `theme/static/misago/css/misago.css` original.

After deploying your new file, run `./appctl collectstatic` to make Misago "collect" this file and replace default with it.


### Example: Adding Google Analytics tracking script

To add custom JavaScript to your Misago site, you will need to override one of Misago's [default templates](https://github.com/rafalp/Misago/blob/master/misago/templates/). There is quite a few to pick from, but of special interest to us are two templates that Misago implements, that are purposefully empty: `scripts.html` and `jumbotron.html`.

The `scripts.html` template is included after Misago's default JavaScripts, but before this JavaScript is being run.
The `jumbotron.html` template is included right before the navbar. Its intention is to provide a place for developers to implement custom branded header or banner.

Because the sooner our analytics script is executed, the better, we will use the `jumbotron.html`.

Go to `misago/theme/templates`. Your template location relative to this path should be same as default template to `misago/templates`, so you will need to create file on following path:

```
misago/theme/templates/misago/jumbotron.html
```

Now you can place your tracking JavaScript inside the `jumbotron.html` you have just created!

Because templates are stored in process memory once loaded, you will need to run `./appctl rebuild` to rebulid Misago container and make it load your template instead of default.


### Sticking a fork into the repo

If you are familiar with Python/Django applications or Docker images involved and wish to customise your setup further, please feel free to branch off/fork the repo - it's simple enough that merging eventual changes from upstream shouldn't be much of an issue.


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

Extends [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) Docker image to disable TLSv1.0 encryption server-wide.


### `/wizard`

Python scripts that `./appctl` runs when it needs to create or change `.env` files with configuration.


Conserving disk space
---------------------

Docker overhead on CPU and memory is negligible, but same can't be said about its disk usage. `./appctl` tries to cleanup whenever possible, but to be safe you will have to monitor amount of free space left on your server, and clean up once in a while using commands like `docker-compose image prune`, manually emptying older logs and backups stored in `logs` and `backups` directories.

Default cron task will also try to delete log files older than 60 days, and backup files that are older than 21 days, and have filename starting with `auto-`.


Need help?
----------

If you have problems setting up your site using `misago_docker`, feel free to ask on [our forums](https://misago-project.org/) or [Discord Chat](https://discord.gg/fwvrZgB). Please don't use Github issues!


Contributing
------------

If you found a bug, issue, or place for improvement, please open an issue or pull request.


Copyright and license
---------------------

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.
