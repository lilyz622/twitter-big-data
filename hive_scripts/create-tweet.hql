CREATE
TABLE IF NOT EXISTS
tweets
(
id int,
retweeted string,
tweet_id string,
user_id string,
screen_name string,
created_at timestamp,
text string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY
'\t'
STORED AS TEXTFILE;

load
data
inpath
'/data/tweets/users.dat'
into table 
users
;
