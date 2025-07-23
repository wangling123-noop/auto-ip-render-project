from bs4 import BeautifulSoup
from utils.request_utils import make_request, proxies  # 导入代理配置

def crawl_dangdang_price(book_name):
    url = f"http://search.dangdang.com/?key={book_name}&act=input"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    # 传入代理参数
    response = make_request(url, headers=headers, proxies=proxies)
    if response is None:
        return "当当价格获取失败"

    soup = BeautifulSoup(response.text, "lxml")
    try:
        price_span = soup.select_one('p.price span')
        if price_span:
            price = price_span.get_text(strip=True)
            return price
        else:
            return "当当价格未找到"
    except Exception as e:
        return f"解析失败: {e}"
