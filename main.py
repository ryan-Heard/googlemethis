import argparse
import csv
import google_search
import logging
import praw
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('error.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

print('=======================================')
parser = argparse.ArgumentParser(description='Use Reddit Bot')
parser.add_argument("-u", "--User", type=str,
                    help='Reddit User Name')

parser.add_argument("-p", "--Password", type=str,
                    help='Reddit User Password')

parser.add_argument("-s", "--Secret", type=str,
                    help='Reddit Application Secret')

parser.add_argument("-cid", "--ClientID", type=str,
                    help='Reddit Application ID')

args = parser.parse_args()


r = praw.Reddit(user_agent="googleMeThis by /u/deadStarman",
                client_id=args.ClientID,
                client_secret=args.Secret)
try:
    r.login(args.User, args.Password, disable_warning=True)
except Exception as e:
    logger.info(e)

trigger_text = ["GoogleMeThis!", "googlemethis!"]
new_comment = []

with open('googleme_cache.txt', 'r', newline='\n') as f:
    cache = list(f.readlines())
    cache = [x.strip() for x in cache]


def run_bot():
    subreddit = r.subreddit("test")
    comments = subreddit.comments(limit=100)
    print("grabbing comment .....")

    for comment in comments:
        comment_clean = comment.body.lower()
        isMatch = any(string in comment_clean for string in trigger_text)
        if isMatch and comment.id not in cache:
            phrase = comment_clean.split('googlemethis!')
            print("Match found!")
            results = google_search.basic_usage(phrase[1])
            comment.reply(results)
            new_comment.append(comment.id)
            cache.append(comment.id)
            time.sleep(60)

while True:
    run_bot()

    if len(new_comment) > 0:
        with open('googleme_cache.txt', 'a', newline='\n') as fp:
            for comment_id in new_comment:
                a = fp.writelines(comment_id + '\n')

        new_comment = []
    time.sleep(2.5)
