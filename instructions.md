************************************************
To run twitter_capture.py:

1. first edit config.py with your configuration 
2. run the below in command after navigating to the directory the file is in

mkdir data
python twitter_capture.py -q apple -d data <-s True>

(add "> /dev/null" to command above for no output)
(-s is optional; use -s True to stream tweets into database)

It will produce the list of tweets for the query "apple" in the file data/stream_apple.json



************************************************
To access a folder on your computer from the vm:

1. follow steps 1-13 from: http://theholmesoffice.com/how-to-share-folders-between-windows-and-ubuntu-using-vmware-player/
2. Shared folders in appear in the location /mnt/hgfs

************************************************
Installing packages python 2.7 on vm:

1. pip install -r requirements.txt

************************************************
To run the bash script on your vm and sqoop mysql table into hive:

1. Do the above first
2. navigate to  /mnt/hgfs/twitter-big-data
3. run the twitter_capture.py to stream data into your vm mysql
4. run the following in terminal:

chmod a+x ./sqoop-into-hadoop.sh
./sqoop-into-hadoop.sh
