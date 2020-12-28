import calendar
from sub_object import result
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
NAME = 0
LIST = 1

def main():
  to_array = []
  for sub_name in result.keys():
    sub = result[sub_name]
    sub_obj = []
    for dt in sub.keys():
      day = int(dt[0])
      time = dt[1:]
      sub_obj.append(dt)
    to_array.append([sub_name, sub_obj])

  writeup(to_array)

def writeup(sub_array):
  rows = []
  num_times = len(sub_array[0][LIST])

  # assumes that "crawl.py" is used to make the object, 
  # since it's got a weird format.
  for idx in range(num_times):
    for sub in sub_array:
      sub_name = sub[NAME]
      timestamp = sub[LIST][idx]
      dayOfWeek = int(timestamp[0])
      weekOfMonth = WEEK * idx
      hour = timestamp[1:] + ':' + str("%02d" % random.randint(0, 60)) # hour + randomized minute
      date = datetime.date.today() + datetime.timedelta(dayOfWeek + weekOfMonth)
      fmt_date = date.strftime('%Y-%m-%d')
      row = {
        'id': '',                 # empty; Cronnit auto-fills
        'title': '[f] [oc]',      # sorta empty; manually filled
        'body': '',               # empty; manually filled imgur link
        'subreddit': sub_name,
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
