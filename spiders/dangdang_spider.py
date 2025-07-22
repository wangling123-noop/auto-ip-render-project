from bs4 import BeautifulSoup
from utils.request_utils import make_request

def crawl_dangdang_price(book_name):
    url = f"http://search.dangdang.com/?key={book_name}&act=input"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = make_request(url, headers=headers)
    if response is None:
        return "当当价格获取失败"

    soup = BeautifulSoup(response.text, "lxml")
    try:
        # 当当价格一般在 <p class="price"><span>价格</span></p>
        price_span = soup.select_one('p.price span')
        if price_span:
            price = price_span.get_text(strip=True)
            return price
        else:
            return "当当价格未找到"
    except Exception as e:
        return f"解析失败: {e}"
