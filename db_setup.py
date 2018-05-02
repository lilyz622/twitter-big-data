import json
from mysql import connector
import mysql.connector
from mysql.connector import errorcode
import config
from dateutil import parser

class Db():
    def __init__(self):
        """Creates necessary db and table if they don't exist"""
        self.create_table()

    def parse_tweet(self, json_str):
        t = json.loads(json_str)
        if 'id_str' in t :
            tweet_id = str(t['id_str']).encode('utf8','ignore')
            user_id = str(t["user"]["id_str"]).encode('utf8','ignore')
            screen_name = str(t['user']['screen_name']).encode('utf8','ignore')
            created_at = parser.parse(t['created_at']).strftime('%Y-%m-%d %H:%M:%S')
            lang = str(t['lang']).encode('utf8','ignore')
            retweeted = "TRUE" if 'retweeted_status' in t else "FALSE"
            text = t['text'].encode('utf8','ignore')
            return (lang, retweeted, tweet_id, user_id, screen_name, created_at, text)
        else: 
            return ("NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL")


    def store_tweet(self, json_str):
        db=mysql.connector.connect(host=config.HOST, user=config.USER, passwd=config.PASSWD, db=config.DATABASE, charset="utf8")
        cursor = db.cursor()
        lang, retweeted, tweet_id, user_id, screen_name, created_at, text = self.parse_tweet(json_str)
        if lang == "en":
            insert_query = 'INSERT INTO tweet \
            (lang, retweeted, tweet_id, user_id, screen_name, created_at, text) \
            VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")'
            cursor.execute(insert_query, (lang, retweeted, tweet_id, user_id, screen_name, created_at, text))
            db.commit()
            cursor.close()
            db.close()
            print('SUCCESS: INSERTED:'+tweet_id+' FROM: '+screen_name)
        return

    def create_database(self, cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(config.DATABASE))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_table(self):
        db = mysql.connector.connect(host=config.HOST, user=config.USER, passwd=config.PASSWD, charset='utf8')
        cursor = db.cursor()

        # create database if database doesn't exist
        try:
            db.database = config.DATABASE
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(cursor)
                db.database = config.DATABASE
            else:
                print(err)
                exit(1)

        # create table if table doesn't exist
        ddl = "CREATE TABLE `%s` (                        \
                `id` int(11) NOT NULL AUTO_INCREMENT,     \
                `query` varchar(25) DEFAULT NULL,         \
                `lang` varchar(10) DEFAULT NULL,          \
                `retweeted` varchar(40) DEFAULT NULL,     \
                `tweet_id` varchar(250) DEFAULT NULL,     \
                `user_id` varchar(128) DEFAULT NULL,      \
                `screen_name` varchar(128) DEFAULT NULL,  \
                `created_at` timestamp NULL DEFAULT NULL, \
                `text` text,          PRIMARY KEY (`id`)  \
                ) AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;" %(config.TABLE)
        try:
            print("Checking if table '%s' exists: "%(config.TABLE))
            cursor.execute(ddl)
            print("table created.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        db.commit()
        cursor.close()
        db.close()
