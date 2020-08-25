# app here: https://www.reddit.com/prefs/apps/

from datetime import datetime
from collections import defaultdict
import praw
import tokens # reddit API keys
from subs import categories   # my secret collection of subs to post to :-)
import csv
import sys

def run(sub_limit, num_times):
  reddit = praw.Reddit(client_id=tokens.client_id,
                      client_secret=tokens.client_secret,
                      password=tokens.password,
                      user_agent=tokens.user_agent,
                      username=tokens.username)

  # set up csv format
  fieldnames = ['sub', 'time', 'posts']
  filename = datetime.now().strftime('%Y-%m-%d') + '.csv'

  with open(filename, mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # categories = { categoryA : [subreddit1, subreddit2, ...],
    #                     categoryB : [subreddit3, subreddit4, ...],
    #                   }
    for c in categories.keys():
      print('working on category: ' + c)
      for sub in categories[c]:
        f_sub ='/r/' + sub
        d = defaultdict(int)

        # get top submissions of the month; store what hour/day they were posted
        for submission in reddit.subreddit(sub).top("month", limit=sub_limit):
            time = int(submission.created_utc)
            time_str = datetime.utcfromtimestamp(time).strftime('%w %H')
            d[time_str] += 1

        # write most successful hour/day combinations to CSV
        best_times = sorted(d, key=d.get, reverse=True)[:num_times]
        for k in best_times:
          writer.writerow({'sub': f_sub, 'time': k, 'posts': str(d[k])})


def main():
  a = sys.argv
  sub_limit = 300
  num_times = 5
  if len(a) >= 2:
    if (a[1] == "--help"):
      print(" crawl.py \n usage: python3 crawl.py [sub_limit] [num_times] \n default: python3 crawl.py 300 5")
      return
    else:
      sub_limit = int(a[1])
  if len(a) >= 3:
    num_times = int(a[2])

  subs = 0
  for k in categories.keys():
    subs += len(categories[k])
  print("using " + str(subs) + " total subs.")
  run(sub_limit, num_times)

if __name__ == "__main__":
  main()

