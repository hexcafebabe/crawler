# crawling reddit posts for optimal times #
this tool takes a batch of subreddits and outputs the most upvoted day+hour combinations per subreddit to a CSV.

## usage ##
there are two optional commandline args: 
1. sub_limit, which is the number of posts to analyze per month. default=300
  1. 1000 is a little better but 300 seems representative.
2. num_times, which is the number of top-performing day+hour combinations to write. default=5

## files not uploaded ##
crawl.py uses my reddit tokens from a file called tokens.py to create a reddit instance.
I have a python dict of strings: `{ category : [subreddits] }` that I want to analyze in subs.py.