#!/bin/bash

# set $GEEKBOOK_NOTES_PATH in .bashrc/.zshrc to the place where you keep your notes

DATE=`date '+%y%m%d'`

#00 06 * * * ble ble ble
echo $DATE
cd $GEEKBOOK_NOTES_PATH

git add *md
git add *org

git commit -m "$DATE: auto-update" 

