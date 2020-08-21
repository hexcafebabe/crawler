# app here: https://www.reddit.com/prefs/apps/

from datetime import datetime
from collections import defaultdict
import praw
import tokens # reddit API keys
import post   # my secret collection of subs to post to :-)

def main():
  reddit = praw.Reddit(client_id=tokens.client_id,
                      client_secret=tokens.client_secret,
                      password=tokens.password,
                      user_agent=tokens.user_agent,
                      username=tokens.username)

  for c in post.categories.keys():
    print('category: ' + c)
    for sub in post.categories[c]:
      print('\tsub: /r/' + sub)
      d = defaultdict(int)

      # 300 seems fairly representative atm
      for submission in reddit.subreddit(sub).top("month", limit=300):
          time = int(submission.created_utc)
          time_str = datetime.utcfromtimestamp(time).strftime('%a %H:00')
          d[time_str] += 1

      best_times = sorted(d, key=d.get, reverse=True)[:5]
      for k in best_times:
        print('\t\t' + k + ', with ' + str(d[k]) + ' posts.')

if __name__ == "__main__":
  main()