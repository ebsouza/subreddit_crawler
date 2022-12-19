# -*- coding: utf-8 -*-

import unittest

from crawler import RedditExtractor


class RedditExtractorTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://old.reddit.com/"
        self.html_page = open("test-assets/page.html", "r")
        self.extractor = RedditExtractor(self.base_url, self.html_page)

    def tearDown(self):
        self.html_page.close()

    def test_extract_parent_element(self):
        thread_info_list = self.extractor.extract_thread_info()

        self.assertEqual(len(thread_info_list), 29)

    def test_extract_parent_element_empty_page(self):
        extractor = RedditExtractor(self.base_url, "<html></html>")
        thread_info_list = extractor.extract_thread_info()

        self.assertEqual(len(thread_info_list), 0)

    def test_extract_thread_info_keys(self):
        thread_info = self.extractor.extract_thread_info()[0]

        self.assertIn("id", thread_info)
        self.assertIn("title", thread_info)
        self.assertIn("likes", thread_info)
        self.assertIn("link", thread_info)
        self.assertIn("comments", thread_info)


if __name__ == '__main__':
    unittest.main()
