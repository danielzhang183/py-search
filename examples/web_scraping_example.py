#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web爬虫示例

演示如何使用py_search进行网页爬取
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_search.web_scraper import WebScraper, scrape_and_save, clean_text, extract_emails


def example_basic_scraping():
    """示例1: 基础爬取"""
    print("=" * 60)
    print("示例1: 基础网页爬取")
    print("=" * 60)
    
    scraper = WebScraper()
    
    # 爬取网页
    url = "https://httpbin.org/html"
    print(f"\n正在爬取: {url}")
    response = scraper.get(url)
    
    if response:
        print(f"✓ 请求成功，状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)} 字符")
        
        # 解析HTML
        soup = scraper.parse_html(response.text)
        if soup:
            title = soup.find('title')
            h1 = soup.find('h1')
            print(f"标题: {title.get_text(strip=True) if title else '未找到'}")
            print(f"H1: {h1.get_text(strip=True) if h1 else '未找到'}")
    else:
        print("✗ 请求失败")


def example_extract_links():
    """示例2: 提取链接"""
    print("\n" + "=" * 60)
    print("示例2: 提取页面链接")
    print("=" * 60)
    
    scraper = WebScraper()
    
    # 使用本地HTML示例
    html = """
    <html>
    <body>
        <h1>示例页面</h1>
        <a href="/page1">页面1</a>
        <a href="https://example.com/page2">页面2</a>
        <a href="/page3">页面3</a>
    </body>
    </html>
    """
    
    soup = scraper.parse_html(html)
    if soup:
        links = scraper.extract_links(soup, base_url="https://example.com")
        print(f"\n找到 {len(links)} 个链接:")
        for link in links:
            print(f"  - {link['text']}: {link['url']}")


def example_css_selector():
    """示例3: 使用CSS选择器"""
    print("\n" + "=" * 60)
    print("示例3: CSS选择器提取")
    print("=" * 60)
    
    html = """
    <html>
    <body>
        <div class="product">
            <h2 class="title">产品1</h2>
            <span class="price">$99.99</span>
        </div>
        <div class="product">
            <h2 class="title">产品2</h2>
            <span class="price">$199.99</span>
        </div>
    </body>
    </html>
    """
    
    scraper = WebScraper()
    soup = scraper.parse_html(html)
    
    if soup:
        # 提取所有产品标题
        titles = scraper.extract_by_selector(soup, '.product .title')
        prices = scraper.extract_by_selector(soup, '.product .price')
        
        print("\n提取的产品信息:")
        for title, price in zip(titles, prices):
            print(f"  - {title}: {price}")


def example_data_cleaning():
    """示例4: 数据清洗"""
    print("\n" + "=" * 60)
    print("示例4: 数据清洗")
    print("=" * 60)
    
    # 测试文本
    dirty_text = "  价格：$99.99\n\n联系邮箱：contact@example.com  \n  "
    print(f"原始文本: {repr(dirty_text)}")
    
    # 清洗文本
    clean = clean_text(dirty_text)
    print(f"清洗后: {repr(clean)}")
    
    # 提取邮箱
    emails = extract_emails(dirty_text)
    print(f"提取的邮箱: {emails}")


def example_save_to_csv():
    """示例5: 保存到CSV"""
    print("\n" + "=" * 60)
    print("示例5: 爬取并保存到CSV")
    print("=" * 60)
    
    # 使用便捷函数
    url = "https://httpbin.org/html"
    output_file = "scraped_data.csv"
    
    # 定义选择器（根据实际网站调整）
    selectors = {
        'title': 'title',
        'h1': 'h1'
    }
    
    print(f"\n正在爬取: {url}")
    success = scrape_and_save(url, output_file, selectors=selectors)
    
    if success:
        print(f"✓ 数据已保存到: {output_file}")
        # 读取并显示
        import csv
        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(f"  数据: {row}")
    else:
        print("✗ 爬取失败")


if __name__ == "__main__":
    print("Web爬虫示例\n")
    print("注意: 某些示例需要网络连接")
    print("=" * 60)
    
    # 运行示例
    example_basic_scraping()
    example_extract_links()
    example_css_selector()
    example_data_cleaning()
    example_save_to_csv()
    
    print("\n" + "=" * 60)
    print("安装依赖:")
    print("  pip install requests beautifulsoup4 lxml fake-useragent")
    print("=" * 60)
    print("\n更多学习资源请查看: docs/WEB_SCRAPING_GUIDE.md")
