# libraries
from datetime import datetime
import calendar
from collections import defaultdict
import praw
import csv
import sys

# personal files
import tokens
from subs import categories

def run(sub_limit, num_times):
  master_list = {}
  reddit = praw.Reddit(client_id=tokens.client_id,
                      client_secret=tokens.client_secret,
                      password=tokens.password,
                      user_agent=tokens.user_agent,
                      username=tokens.username)

  # set up csv format
  fieldnames = ['sub', 'time', 'posts']
  filename = datetime.now().strftime('sorted_%Y-%m-%d') + '.csv'

  for c in categories.keys():
    print('working on category: ' + c)
    for sub in categories[c]:
      formatted_sub = '/r/' + sub
      print('\t' + formatted_sub)
      d = defaultdict(int)
      scores = defaultdict(int)

      # get top submissions of the month; store what hour/day they were posted AND
      # how many upvotes they got
      for submission in reddit.subreddit(sub).top("month", limit=sub_limit):
          time = int(submission.created_utc)
          time_str = datetime.utcfromtimestamp(time).strftime('%w %H')
          d[time_str] += 1
          scores[time_str] += int(submission.score)

      # write most successful hour/day combinations to dict
      successes = {}
      best_times = sorted(d, key=d.get, reverse=True)[:num_times]
      for time in best_times:
        successes[time] = scores[time]

      master_list[formatted_sub] = successes

  with open("sub_object.py", "a") as f:
    print('result = ', end='', file=f)
    print(str(master_list), file=f)

def setup():
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
  return sub_limit, num_times

def main():
  sub_limit, num_times = setup()
  run(sub_limit, num_times)

if __name__ == "__main__":
  main()

