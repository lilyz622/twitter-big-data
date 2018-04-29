# To run this code, first edit config.py with your configuration, then:
#
# mkdir data

# python twitter_capture.py -q apple -d data (-s True)
# (add "> /dev/null" to command above for no output)
# (-s is optional; use -s True to stream tweets into database)
#
# It will produce the list of tweets for the query "apple"

# in the file data/stream_apple.json

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import time
from db_setup import Db

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")

    parser.add_argument("-s",
                        "--is-storing-to-db",
                        required = False,
                        choices = [True, False],
                        type = bool,
                        dest="is_storing_to_db",
                        help="twitter.tweet")
    parser.add_argument("-t",
                        "--timeout",
                        required = False,
                        dest="timeout",
                        help="twitter.tweet")

    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""


    def __init__(self, data_dir, query, is_storing_to_db, timeout):
        query_fname = format_filename(query)
        self.t_end = time.time() + int(timeout)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)
        if is_storing_to_db:
            self.db = Db()
        else:
            self.db = False


    def on_data(self, data):
        if time.time() < self.t_end:
            try:
                with open(self.outfile, 'a') as f:
                    f.write(data)
                    #print(data)
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                time.sleep(5)
            if self.db != False:
                try:
                    self.db.store_tweet(data)
                except:
                    print("Error on_data storage")
                    time.sleep(5)

            return True
        else:
            return False

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


def format_filename(fname):
    """Convert file name into a safe string.

    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.

    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status



if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
    api = tweepy.API(auth)

    twitter_stream=Stream(auth, MyListener(args.data_dir, args.query, args.is_storing_to_db, args.timeout))
    twitter_stream.filter(track=[args.query])

    twitter_stream.disconnect() # that should wait until next tweet, so let's delete it
    del twitter_stream
