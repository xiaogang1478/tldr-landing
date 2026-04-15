#!/usr/bin/env python3
"""
MVP爬虫 - 使用Playwright处理知乎
"""
from playwright.sync_api import sync_playwright
import json
import time
import random

def search_zhihu(keyword):
    """搜索知乎"""
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 搜索
        url = f"https://www.zhihu.com/search?type=content&q={keyword}"
        print(f"搜索: {keyword}")
        
        try:
            page.goto(url, timeout=20000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            
            # 滚动加载
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 500)")
                time.sleep(1)
            
            # 提取问题卡片
            cards = page.query_selector_all(".List-item, .ContentItem")
            
            for card in cards[:10]:
                try:
                    # 提取标题
                    title_elem = card.query_selector("h2, .ContentItem-title")
                    title = title_elem.inner_text() if title_elem else ""
                    
                    # 提取摘要
                    excerpt_elem = card.query_selector(".RichText, .ContentItem-excerpt")
                    excerpt = excerpt_elem.inner_text() if excerpt_elem else ""
                    
                    # 提取链接
                    link_elem = card.query_selector("a[href*='/question/']")
                    href = link_elem.get_attribute("href") if link_elem else ""
                    
                    if title and len(title) > 5:
                        results.append({
                            "title": title.strip(),
                            "excerpt": excerpt.strip()[:200],
                            "url": f"https://www.zhihu.com{href}" if href else ""
                        })
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"失败: {e}")
        
        browser.close()
    
    return results

if __name__ == "__main__":
    # 测试
    keyword = "受不了"
    results = search_zhihu(keyword)
    
    print(f"\n找到 {len(results)} 条结果:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title'][:40]}")
        print(f"   {r['excerpt'][:60]}...")
        print()