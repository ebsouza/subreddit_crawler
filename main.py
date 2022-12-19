# -*- coding: utf-8 -*-

import argparse

from src.crawler import RedditCrawler
from src.utils import thread_info_to_string

parser = argparse.ArgumentParser(description='Reddit Crawler')
parser.add_argument('--subreddits',
                    dest='subreddits',
                    default=None,
                    type=str,
                    help='Subthreads list as string. Ex: Home;AskReddit;Minecraft')
parser.add_argument('--like_threshold',
                    dest='like_threshold',
                    default=0,
                    type=int,
                    help='A threshold to filter threads by votes')
args = parser.parse_args()

for subreddit in args.subreddits.split(";"):

    print(f"[Starting scraping: '{subreddit}']")

    try:
        crawler = RedditCrawler(subreddit, args.like_threshold)
        crawler.run()
    except Exception as e:
        print(f"Sorry. It was not possible run the crawler. Reason : {e}")
        continue

    print(f"[Finishing scraping: '{subreddit}']")

    print("[Results] - Sorted by likes")
    for thread_info in crawler.sorted_threads_info():
        index = crawler.sorted_threads_info().index(thread_info)
        thread_info_str = thread_info_to_string(
            thread_info, index + 1, ["title", "likes", "link", "comments"])
        try:
            print(thread_info_str)
        except UnicodeEncodeError:
            print("Invalid character!")
