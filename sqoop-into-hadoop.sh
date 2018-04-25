#!/bin/bash

# INSTRUCTIONS
# to be run in your virtual machine - navigate to "/mnt/hgfs/twitter-big-data"
# chmod a+x ./sqoop-into-hadoop.sh # run this before you run the script

# start services
#$DEV1/scripts/training_setup_dev1.sh
#sudo service zookeeper-server start
#sudo service hive-server2 start
#sudo service hue stop
#sudo service hue start

# check if table is where we want it
tables=$(sqoop list-tables --connect jdbc:mysql://localhost/twitter --username training --password training)
echo "Current tables in twitter db: $tables"

# sqoop if table exists in mysql
table="tweet"
if [[ $tables = *$table* ]]; then

# delete table in hive
beeline -u jdbc:hive2://localhost:10000 -n training -p training -f ./hive_scripts/delete-tweet.hql

# create twitter db in hive
beeline -u jdbc:hive2://localhost:10000 -n training -p training -f ./hive_scripts/create-twitter.hql


# update tweet set text=replace(replace(text, '\r',''), '\n','');
# sqoop into twitter.tweets in hive on hdfs
sqoop import --connect jdbc:mysql://localhost/twitter --username training --password training --table tweet --null-non-string '\\N' --hive-import --hive-table twitter.tweets

fi

