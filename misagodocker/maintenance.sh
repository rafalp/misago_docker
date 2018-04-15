#!/usr/bin/env bash

# This is the cron job that does the scheduled maintenace on the Misago.
# It deletes old sessions, refreshes active posters list, prunes categories
# set to delete old threads, keeps read tracking record small, disables
# expired bans, etc. ect.
#
# Tasks defined in this file are ran serially, one after another, making it
# simpler to keep things in order (eg. active posters list is populated after
# specified categories are pruned) and their memory usage is in check (no more
# than single maintenance task is running at single time)
#
# You are free to edit this file to add custom `manage.py` calls for your site.
 
python manage.py prunecategories
python manage.py buildactivepostersranking
python manage.py clearattachments
python manage.py clearreadtracker
python manage.py clearsessions
python manage.py invalidatebans
python manage.py deletemarkedusers