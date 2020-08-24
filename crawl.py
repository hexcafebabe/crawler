# app here: https://www.reddit.com/prefs/apps/

from datetime import datetime
from collections import defaultdict
import praw
import tokens # reddit API keys
import subs   # my secret collection of subs to post to :-)
import csv
import sys

def main():
  sub_limit, num_times = set_limits()
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

    # subs.categories = { categoryA : [subreddit1, subreddit2, ...],
    #                     categoryB : [subreddit3, subreddit4, ...],
    #                   }
    for c in subs.categories.keys():
      print('working on category: ' + c)
      for sub in subs.categories[c]:
        f_sub ='/r/' + sub
        d = defaultdict(int)

        # get top submissions of the month; store what hour/day they were posted
        for submission in reddit.subreddit(sub).top("month", limit=sub_limit):
            time = int(submission.created_utc)
            time_str = datetime.utcfromtimestamp(time).strftime('%a %H:00')
            d[time_str] += 1

        # write most successful hour/day combinations to CSV
        best_times = sorted(d, key=d.get, reverse=True)[:num_times]
        for k in best_times:
          writer.writerow({'sub': f_sub, 'time': k, 'posts': str(d[k])})


def set_limits():
  a = sys.argv
  sub_limit = 300
  num_times = 5
  if len(a) >= 2:
    sub_limit = int(a[1])
  if len(a) >= 3:
    num_times = int(a[2])
  return sub_limit, num_times

if __name__ == "__main__":
  main()

