import sys
import csv
import datetime
from collections import defaultdict
import random

# field names required for Cronnit
fieldnames = ['id','title','body','subreddit','date','time',
  'timezone','nsfw','sendreplies','delete']

SUNDAY = 6
WEEK = 7

capped = defaultdict(int)

def main():
  a = sys.argv
  if len(a) < 2:
    print('error: put filename on cmdline')
  else:
    if (a[1] == '--help'):
      print(" schedule.py \n usage: python3 schedule.py file.csv [start_date] \n default: python3 schedule.py file.csv next_sunday")
      return

    today = datetime.date.today()
    if len(a) < 3:
      print('default: starting scheduling from next sunday.')
      start_date = today + datetime.timedelta(today.weekday()+SUNDAY % WEEK)
      read(a[1], start_date)
    else: 
      print('starting scheduling from ' + a[2] + ' days from today.')
      start_date = today + datetime.timedelta(int(a[2]))
      read(a[1], start_date)

# if there are too many posts on a day, just bump it to a week later.
def upDate(date):
  ctr = 0
  while (capped[date] > 3):
    date = date + datetime.timedelta(weeks=1)
    ctr += 1
    print("bumped " + str(ctr) + " times")
  capped[date] += 1
  return date

def read(filename, start_date):
  rows = []
  with open(filename) as csv_file:
    reader = csv.DictReader(csv_file)

    # assumes that "crawl.py" is used to make the csv_file, 
    # since it's got a weird format.
    for row in reader:
      split = row['time'].split(' ')
      dayOfWeek = int(split[0])
      weekOfMonth = WEEK * random.randint(0,3)
      hour = split[1] + ':' + str("%02d" % random.randint(0, 60)) # hour + randomized minute
      date = start_date + datetime.timedelta(dayOfWeek + weekOfMonth)
      date = upDate(date) 
      fmt_date = date.strftime('%Y-%m-%d')
      row = {
        'id': '',                 # empty; Cronnit auto-fills
        'title': '[f] [oc]',      # sorta empty; manually filled
        'body': '',               # empty; manually filled imgur link
        'subreddit': row['sub'],
        'date': fmt_date,
        'time': hour,
        'timezone': 'GMT-0700',
        'nsfw': 1,                # because I only make NSFW content :) 
        'sendreplies': 1,
        'delete': 0
      }     
      rows.append(row)
      
  write(rows)

def write(rows):
  output = 'upload-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
  with open(output, mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

if __name__ == '__main__':
  main()
