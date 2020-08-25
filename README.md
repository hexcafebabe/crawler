# crawling reddit posts for optimal times #
this is a playground for hexcafebabe to figure out how to be better at reddit. 
the crawler goes through prior reddit posts and saves good times to post for each subreddit to a CSV; 
the scheduler uses that CSV plus a little randomness to create a streamlined posting schedule .

## crawl.py ##
this tool takes a batch of subreddits and outputs the most upvoted day+hour combinations per subreddit to a CSV.
the format is somewhat human-readable; looks like this:
    
```csv
sub,time,posts
/r/abc,1 17,14 
/r/def,4 3,9   
```
explanation:
```python
# /r/abc = subreddit, 1 = Monday, 17 = 5pm, 14 = num of posts in this hour/day combo
# /r/def = subreddit, 4 = Thursday, 3 = 3am, 9 = num of posts in this hour/day combo
```

### usage ###

`python3 crawl.py [sub_limit] [num_times]`

`python3 crawl.py`

`python3 crawl.py 1000 5`

there are two optional commandline args: 
1. sub_limit, which is the number of posts to analyze per month. default=300
2. num_times, which is the number of top-performing day+hour combinations to write. default=5

### files not uploaded ###
crawl.py uses my reddit tokens from a file called tokens.py to create a reddit instance.

I have a python dict of strings: `{ category : [subreddits] }` that I want to analyze in subs.py.

## schedule.py ##
this tool reads the CSV in the format that comes from crawl.py
