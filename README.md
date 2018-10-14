Misago Docker
=============

**WARNING: This repository is work in progress, don't use it yet!**

This repository aims to provide black-box production-quality setup of Misago for people who:

- Want to run their own forum using Misago
- Have a server with Docker lying around
- Know enough of Linux to ssh to VPS, move around, modify files, run programs and follow instructions from guides


Backup and restore
==================

Creating new backup
-------------------

Running the `./appctl backup` will result in new backup being created in `backups` directory, under the path corresponding to year and month of backup's creation (eg. 2018/10 for backups created in october 2018).

Backup will be a `tar.gz` archive named using `misago-YYYYMMDDHHMMSS.tar.gz` format and will contain `database.sql` file with database export created using `pg_dump`, and `media` directory contained user-uploaded files.


Restoring from backup
---------------------

You can restore your site's data by placing the backup archive in the `backups` directory, and running `./appctl restore yourbackupfile.tar.gz`. If your backup file is located in the subdirectory, you can specify the path to it relative to `backups`, eg.: `./appctl restore 2018/10/yourbackupfile.tar.gz`.

Restoration will:

- overwrite your current `media` directory with one from archive.
- load the `database.sql` to `psql`, overwriting existing database tables with ones from file.

**NOTE:** because restoration process can be considered descructive, you should backup any existing data if you are restoring the site that has data you may want to recover if something goes wrong.

After you've restored from backup, it's good idea to follow up with `./appctl rebuild` to rebuild Misago image, giving it's application container a chance to rebuild filesystem caches.


Daily backups
-------------




Need help?
==========

If you have problems setting up your site using `Misago-Docker`, feel free to ask on [our forums](https://misago-project.org/) or [Discord Chat](https://discord.gg/fwvrZgB). Please don't use Github issues!


Copyright and license
=====================

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.
