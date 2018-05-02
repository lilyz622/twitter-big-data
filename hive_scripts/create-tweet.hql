CREATE
<<<<<<< HEAD
TABLE tweets
(
id int,
=======
TABLE IF NOT EXISTS
tweets
(
id int,
retweeted string,
>>>>>>> f7d0529c85907f4dc91f6f36c04ef8fe744818aa
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
<<<<<<< HEAD
OVERWRITE into
table users
=======
into table 
users
>>>>>>> f7d0529c85907f4dc91f6f36c04ef8fe744818aa
;
