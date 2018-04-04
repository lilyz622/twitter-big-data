CREATE
TABLE tweets
(
id int,
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
OVERWRITE into
table users
;
