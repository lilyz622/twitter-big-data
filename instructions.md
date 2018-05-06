************************************************
To run the bash script on your vm and capture tweets and sqoop mysql table into hive:

1. navigate to your unzipped directory
2. run the following in terminal:
NOTE: the default is to capture 10 minutes of tweets
NOTE: you must have a config.py properly configured with your twitter API keys (see config_template.py)

/bin/bash ./sqoop-into-hadoop.sh

************************************************
To run twitter_capture.py:

1. first edit config.py with your configuration 
2. run the below in command after navigating to the directory the file is in
NOTE: you must have a config.py properly configured with your twitter API keys (see config_template.py)

mkdir data
python twitter_capture.py -q trump -d data <-s True> -t 600 

(add "> /dev/null" to command above for no output)
(-s is optional; use -s True to stream tweets into database)
(-t is time of capture in seconds)

It will produce the list of tweets for the query "trump" in the file data/stream_trump.json

************************************************
To access a folder on your computer from the vm:

1. follow steps 1-13 from: http://theholmesoffice.com/how-to-share-folders-between-windows-and-ubuntu-using-vmware-player/
2. Shared folders in appear in the location /mnt/hgfs

************************************************
Installing packages python 2.7 on vm:

1. pip install -r requirements.txt

************************************************
To query data in hive:

% beeline -u jdbc:hive2://localhost:10000/twitter -n training -p training
> select * from tweets limit 1;