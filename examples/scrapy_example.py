#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrapy 快速入门示例

这个文件展示了如何使用 Scrapy 创建一个简单的爬虫。
注意：这只是一个示例，实际使用需要创建完整的 Scrapy 项目。

要创建完整的 Scrapy 项目，请运行：
    scrapy startproject myproject
    cd myproject
    scrapy genspider quotes quotes.toscrape.com
"""

# ============================================================================
# 示例1：最简单的 Scrapy 爬虫
# ============================================================================

"""
# 在 Scrapy 项目中创建 spider (spiders/quotes_spider.py)

import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # 提取所有名言
        quotes = response.css('div.quote')
        
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        # 跟踪下一页链接
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

# 运行：
# scrapy crawl quotes -o quotes.json
"""

# ============================================================================
# 示例2：使用 Item 和 ItemLoader
# ============================================================================

"""
# items.py
import scrapy

class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()

# spiders/quotes_spider.py
import scrapy
from scrapy.loader import ItemLoader
from myproject.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('div.quote')
        
        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css('text', 'span.text::text')
            loader.add_css('author', 'span small.author::text')
            loader.add_css('tags', 'div.tags a.tag::text')
            loader.add_value('url', response.url)
            yield loader.load_item()
"""

# ============================================================================
# 示例3：使用 CrawlSpider（规则爬虫）
# ============================================================================

"""
# spiders/news_spider.py
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from myproject.items import NewsItem

class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/news']
    
    rules = (
        # 提取新闻详情页
        Rule(
            LinkExtractor(allow=r'/news/\d+'),
            callback='parse_news',
            follow=False
        ),
        # 跟踪分类和列表页
        Rule(
            LinkExtractor(allow=r'/category/'),
            follow=True
        ),
    )
    
    def parse_news(self, response):
        loader = ItemLoader(item=NewsItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_css('content', '.content::text')
        loader.add_value('url', response.url)
        yield loader.load_item()
"""

# ============================================================================
# 示例4：使用 Pipeline 保存数据
# ============================================================================

"""
# pipelines.py
import json
import sqlite3
from itemadapter import ItemAdapter

class JsonPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w', encoding='utf-8')
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

class DatabasePipeline:
    def __init__(self):
        self.conn = None
    
    def open_spider(self, spider):
        self.conn = sqlite3.connect('scrapy.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT UNIQUE
            )
        ''')
    
    def close_spider(self, spider):
        self.conn.close()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.conn.execute(
            'INSERT OR IGNORE INTO items (title, url) VALUES (?, ?)',
            (adapter.get('title'), adapter.get('url'))
        )
        self.conn.commit()
        return item

# settings.py
ITEM_PIPELINES = {
    'myproject.pipelines.JsonPipeline': 300,
    'myproject.pipelines.DatabasePipeline': 400,
}
"""

# ============================================================================
# 示例5：自定义 Middleware
# ============================================================================

"""
# middlewares.py
import random

class RandomUserAgentMiddleware:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
        ]
    
    def process_request(self, request, spider):
        ua = random.choice(self.user_agents)
        request.headers['User-Agent'] = ua
        return None

class ProxyMiddleware:
    def __init__(self):
        self.proxies = [
            'http://proxy1:8080',
            'http://proxy2:8080',
        ]
    
    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy
        return None

# settings.py
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.RandomUserAgentMiddleware': 400,
    'myproject.middlewares.ProxyMiddleware': 500,
}
"""

# ============================================================================
# 示例6：处理 JavaScript 渲染页面（使用 Scrapy-Splash）
# ============================================================================

"""
# 安装：pip install scrapy-splash

# settings.py
SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
}

# spiders/js_spider.py
from scrapy_splash import SplashRequest

class JSSpider(scrapy.Spider):
    name = 'js_spider'
    start_urls = ['https://example.com']
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                args={'wait': 0.5}  # 等待JS渲染
            )
    
    def parse(self, response):
        items = response.css('.dynamic-content')
        for item in items:
            yield {'text': item.css('::text').get()}
"""

# ============================================================================
# 示例7：完整的新闻爬虫项目结构
# ============================================================================

"""
项目结构：
news_scraper/
├── scrapy.cfg
└── news_scraper/
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        ├── __init__.py
        └── news_spider.py

创建步骤：
1. scrapy startproject news_scraper
2. cd news_scraper
3. scrapy genspider news example.com
4. 编辑 items.py, spiders/news_spider.py, pipelines.py, settings.py
5. scrapy crawl news -o news.json
"""

if __name__ == '__main__':
    print("=" * 60)
    print("Scrapy 示例代码")
    print("=" * 60)
    print("\n这个文件包含了 Scrapy 的各种使用示例。")
    print("\n要开始使用 Scrapy，请按照以下步骤：")
    print("\n1. 安装 Scrapy:")
    print("   pip3 install scrapy")
    print("\n2. 创建项目:")
    print("   scrapy startproject myproject")
    print("\n3. 创建爬虫:")
    print("   cd myproject")
    print("   scrapy genspider spider_name example.com")
    print("\n4. 运行爬虫:")
    print("   scrapy crawl spider_name -o output.json")
    print("\n详细学习指南请参考：")
    print("   docs/SCRAPY_LEARNING_GUIDE.md")
    print("=" * 60)
