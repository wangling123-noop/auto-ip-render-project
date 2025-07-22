from bs4 import BeautifulSoup
from utils.request_utils import make_request
import urllib.parse

def crawl_jd_price(book_name):
    query = urllib.parse.quote(book_name)
    url = f"https://search.jd.com/Search?keyword={query}&enc=utf-8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = make_request(url, headers=headers)
    if response is None:
        return "京东价格获取失败"

    soup = BeautifulSoup(response.text, "lxml")
    try:
        # 京东价格通常在 <div class="p-price"><strong><i>价格</i></strong></div>
        price_tag = soup.select_one('.p-price strong i')
        if price_tag:
            price = price_tag.get_text(strip=True)
            return price
        else:
            return "京东价格未找到"
    except Exception as e:
        return f"解析失败: {e}"
