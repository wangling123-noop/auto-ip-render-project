import requests
from bs4 import BeautifulSoup
from proxy_pool.premium_proxy import get_kuaidaili_proxy

def crawl_dangdang_price(book_name):
    try:
        url = f"http://search.dangdang.com/?key={book_name}&act=input"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        proxies = get_kuaidaili_proxy()
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if resp.status_code != 200:
            return f"状态码异常：{resp.status_code}"

        soup = BeautifulSoup(resp.text, "lxml")
        price_tag = soup.select_one(".search_prefer_price")
        if price_tag:
            return price_tag.text.strip()
        return "未找到价格"
    except Exception as e:
        return f"请求失败：{e}"
