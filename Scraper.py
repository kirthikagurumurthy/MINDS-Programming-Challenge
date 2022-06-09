import json
from time import mktime
from datetime import datetime
import feedparser as fp
import newspaper
from newspaper import Article
import time

start_time = time.time()
MAX_ARTICLES = 10
articles = {}
articles['news_sites'] = {}
ctr = 1

with open('news_sites.json') as source:
    news_sites = json.load(source)


for news_site_name, val in news_sites.items():
    news = newspaper.build(val['link'], memoize_articles=False)
    all_news = {
        "items": [],
        "link": val['link']

    }

    for content in news.articles:
        if ctr > MAX_ARTICLES:
            break
        try:
            content.download()
            content.parse()
        except Exception as e:
            print(e)
            continue
        if content.publish_date is None:
            ctr = ctr + 1
            continue
        item = {}
        item['title'] = content.title
        item['link'] = content.url
        item['text'] = content.text
        item['published'] = content.publish_date.isoformat()
        all_news['items'].append(item)
        print(ctr, "News_Site:", news_site_name, "\n URL: ", content.url)
        ctr = ctr + 1

    articles['news_sites'][news_site_name] = all_news
    try:
        with open('news_scrape.json', 'w') as op_file:
            json.dump(articles, op_file)
    except Exception as e:
        print(e)

print("Time Taken:")
print("--- %s seconds ---" % (time.time() - start_time))
