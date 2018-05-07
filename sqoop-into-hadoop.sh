#!/bin/bash

# INSTRUCTIONS
# to be run in your virtual machine - navigate to "/mnt/hgfs/twitter-big-data"
# chmod a+x ./sqoop-into-hadoop.sh # run this before you run the script

#Install required python packages
pip install -r requirements.txt

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

#DROP mysql table so that it is fresh for next time.
mysql --user=training --password=training --host=localhost --database=twitter -e 'drop table if exists tweet'

##Execute the map-reduce jobs: Name, Word,BiGram
hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.4.3.jar \
    -mapper WordMapper.py \
    -reducer WordReducer.py \
    -file ./MapReduce/WordMapper.py \
    -file ./MapReduce/WordReducer.py \
    -input /user/hive/warehouse/twitter.db/tweets/* \
    -output output-word

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.4.3.jar \
    -mapper BigramMapper.py \
    -reducer BigramReducer.py \
    -file ./MapReduce/BigramMapper.py \
    -file ./MapReduce/BigramReducer.py \
    -input /user/hive/warehouse/twitter.db/tweets/* \
    -output output-bigram

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.4.3.jar \
    -mapper NameMapper.py \
    -reducer NameReducer.py \
    -file ./MapReduce/NameMapper.py \
    -file ./MapReduce/NameReducer.py \
    -input /user/hive/warehouse/twitter.db/tweets/* \
    -output output-name

#DISPLAY 1st 20 lines sorted descending from each MR job
hdfs dfs -cat output-name/part-00000 | \
    awk '{ print $2 " " $1}' | \
    sort -n -r | \
    head -20

hdfs dfs -cat output-bigram/part-00000 | \
    awk '{ print $3 " " $1$2}' | \
    sort -n -r | \
    head -20

hdfs dfs -cat output-word/part-00000 | \
    awk '{ print $2 " " $1}' | \
    sort -n -r | \
    head -20

echo "The processing is now complete"

fi

