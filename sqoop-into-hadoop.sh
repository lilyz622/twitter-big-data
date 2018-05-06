#!/bin/bash

# INSTRUCTIONS
# to be run in your virtual machine - navigate to "/mnt/hgfs/twitter-big-data"
# chmod a+x ./sqoop-into-hadoop.sh # run this before you run the script

# start services
$DEV1/scripts/training_setup_dev1.sh
sudo service zookeeper-server restart
sudo service hive-server2 restart
sudo service hue restart

#capture the tweets for "-t seconds"
python twitter_capture.py \
    -q trump \
    -d data \
    -s True \
    -t 600


# check if table is where we want it
sqoop_tables=$(sqoop list-tables --connect jdbc:mysql://localhost/twitter --username training --password training)
echo "Current tables in sqoop twitter db: $sqoop_tables"
mysql_tables=$(mysql --user=training --password=training --host=localhost --database=twitter -e 'show tables\G' | grep ":" | cut -f2 -d" ")
echo "Current tables in mysql twitter db: $mysql_tables"

# sqoop if table exists in mysql
table="tweet"
if [[ $sqoop_tables = *$table* && $mysql_tables = *$table* ]]; then

# delete table in hive
#beeline -u jdbc:hive2://localhost:10000 -n training -p training -f ./hive_scripts/delete-tweet.hql

# create twitter db in hive
beeline -u jdbc:hive2://localhost:10000 \
-n training \
-p training \
-f ./hive_scripts/create-twitter.hql

# update tweet set text=replace(replace(text, '\r',''), '\n','');
# sqoop into twitter.tweets in hive on hdfs
sqoop import --direct \
    --connect jdbc:mysql://localhost/twitter \
    --username training --password training \
    --table tweet --null-non-string '\\N' \
    --hive-import --hive-table twitter.tweets

mysql --user=training --password=training --host=localhost --database=twitter -e 'drop table if exists tweet'

fi

