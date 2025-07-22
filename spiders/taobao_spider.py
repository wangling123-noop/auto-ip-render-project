from bs4 import BeautifulSoup
from utils.request_utils import make_request
import urllib.parse

def crawl_taobao_price(book_name):
    query = urllib.parse.quote(book_name)
    url = f"https://s.taobao.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = make_request(url, headers=headers)
    if response is None:
        return "淘宝价格获取失败"

    soup = BeautifulSoup(response.text, "lxml")
    try:
        # 淘宝的价格一般在 class="price" 或类似的标签内，示例取第一个价格
        price_tag = soup.select_one('.price')
        if price_tag:
            price = price_tag.get_text(strip=True)
            return price
        else:
            return "淘宝价格未找到"
    except Exception as e:
        return f"解析失败: {e}"
