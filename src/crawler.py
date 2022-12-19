# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import browser_info, no_data_message_str, no_data_message_int


class RedditExtractor:
    def __init__(self, base_url, html):
        self.base_url = base_url
        self.html = html

    def extract_thread_info(self):
        parent_element = self.__extract_parent_element()
        thread_info_list = list()

        if not parent_element:
            return thread_info_list

        for child_element in parent_element:
            info = dict()

            info['id'] = child_element.get('data-fullname')
            if not info['id']:
                continue

            info['title'] = self.__extract_title(child_element)
            info['likes'] = self.__extract_likes(child_element)
            info['link'] = self.__extract_link(child_element)
            info['comments'] = self.__extract_comments(child_element)

            thread_info_list.append(info)

        return thread_info_list

    def __extract_parent_element(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        parent_element = soup.find("div", {"id": "siteTable"})

        if not parent_element or len(parent_element) == 1:
            return None

        return parent_element

    def __extract_title(self, html_element):
        thread = html_element.find("div", {"class": "entry unvoted"})
        return thread.find("a", {"data-event-action": "title"}).text

    def __extract_likes(self, html_element):
        html_element = html_element.find("div", {"class": "midcol unvoted"})
        likes = html_element.find("div", {"class": "score unvoted"}).get('title')
        try:
            return int(likes)
        except TypeError:
            return no_data_message_int

    def __extract_link(self, html_element):
        thread = html_element.find("div", {"class": "entry unvoted"})
        try:
            link = thread.find("a", {"data-event-action": "title"}).get('href')
            if link.find("https://") != -1:
                return link
            return f"{self.base_url[:-1]}{link}"
        except AttributeError:
            return no_data_message_str

    def __extract_comments(self, html_element):
        thread = html_element.find("div", {"class": "entry unvoted"})
        try:
            return thread.find("a", {"data-event-action": "comments"}).get('href')
        except AttributeError:
            return no_data_message_str


class RedditCrawler:

    base_url = 'https://old.reddit.com/'

    def __init__(self, subreddit, likes_threshold=0):
        self.threads = list()
        self.url = f"{self.base_url}r/{subreddit}/"
        self.likes_threshold = likes_threshold

    def run(self, page_limit=1000):
        page_generator = self.__next_page_generator()
        next_url = next(page_generator)
        response = requests.get(next_url, headers={"User-Agent": browser_info})

        count_pages = 0

        while response.status_code == 200:

            extractor = RedditExtractor(self.base_url, response.content)
            count_pages += 1

            print(f"Scraping page : {count_pages} | url : {next_url}")

            thread_info_list = extractor.extract_thread_info()
            if thread_info_list:
                self.__update_threads_list(thread_info_list)
            else:
                break

            next_url = self.__get_next_url(page_generator, thread_info_list[-1]['id'])
            response = requests.get(next_url, headers={"User-Agent": browser_info})

            if count_pages >= page_limit:
                break

    def sorted_threads_info(self):
        from operator import itemgetter
        return sorted(self.threads, key=itemgetter("likes"), reverse=True)

    def __get_next_url(self, page_generator, last_thread_id):
        next_url = next(page_generator)
        next_url += f"&after={last_thread_id}"
        return next_url

    def __next_page_generator(self):
        yield self.url
        count = 0
        while True:
            count += 25
            yield f"{self.url}?count={count}"

    def __update_threads_list(self, thread_info_list):
        for thread_info in thread_info_list:
            likes = thread_info["likes"]
            if likes >= self.likes_threshold:
                self.threads.append(thread_info)
