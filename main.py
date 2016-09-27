import csv
import praw
import time
import google_search
import argparse


print('=======================================')
parser = argparse.ArgumentParser(description='Use Reddit Bot')

parser.add_argument('User', type=str,
                    help='Reddit User Name')

parser.add_argument('Password', type=str,
                    help='Reddit User Password')

args = parser.parse_args()

r = praw.Reddit(user_agent="googleMeThis by /u/deadStarman")
r.login(args.User, args.Password, disable_warning=True)
trigger_text = ["GoogleMeThis!", "googlemethis!"]
new_comment = []

with open('googleme_cache.txt', 'r', newline='\n') as f:
    cache = list(f.readlines())
    cache = [x.strip() for x in cache]


def run_bot():
    subreddit = r.get_subreddit("test")
    comments = subreddit.get_comments(limit=100)
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
