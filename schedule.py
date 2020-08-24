import sys
import csv
import datetime
import random

# days = {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}


def main():
  a = sys.argv
  if len(a) < 2:
    print("error: put filename on cmdline")
  else:
    read(a[1])


def read(filename):
  # start posting from the following sunday
  today = datetime.date.today()
  sunday = today + datetime.timedelta(today.weekday()+6 % 7)

  with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      split = row['time'].split(' ')
      dayOfWeek = int(split[0])
      weekOfMonth = 7 * random.randint(0,3)
      hour = split[1]
      date = sunday + datetime.timedelta(dayOfWeek + weekOfMonth) 
      print(date.strftime('%A, %B %-d'), hour)


if __name__ == "__main__":
  main()
