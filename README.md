## RedditCrawler

![](assets/crawler_running.gif)

### 1. Setup

1. Local Environment

```
python3 -m venv reddit_crawler
```

```
source reddit_crawler/bin/active
```

```
(reddit_crawler) pip install --upgrade pip
```

```
(reddit_crawler) pip install -r requirements.txt
```

2. Docker

```
docker build --tag=crawler:reddit .
```

```
docker create -t -i --name reddit_crawler -v <user_workspace>:/home/user crawler:reddit
```

```
docker start reddit_crawler
```

```
docker exec -it reddit_crawler bash -c "python3 main.py --subreddits cats --like_threshold 500"
```


### 2. Scraping old.reddit subreddits

Filtering threads over 500 likes( *--like_threshold* ) on cats and AskReddit subreddits ( *--subreddits*) and send that via telegram(*--telegram*)

```
# Local environment
python main.py --subreddits 'cats;AskReddit' --like_threshold 500 --telegram
```

```
# Docker
docker start reddit_crawler
docker exec -it reddit_crawler bash -c "python3 main.py --subreddits 'cats;AskReddit' --like_threshold 500 --telegram"
```

## Tests

```
# Local environment
(reddit_crawler) python tests.py

# Docker
docker start reddit_crawler
docker exec -it reddit_crawler bash -c "python3 tests.py"
```