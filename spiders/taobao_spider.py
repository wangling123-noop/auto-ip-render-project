# spiders/taobao_spider.py
from bs4 import BeautifulSoup
from app import make_request

def crawl_taobao_price(book_name):
    url = f"https://s.taobao.com/search?q={book_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = make_request(url, headers=headers)
    if response is None:
        return "淘宝价格获取失败"

    soup = BeautifulSoup(response.text, "lxml")

    # 简单示范：找第一个价格，淘宝的结构比较复杂，这里只是示例
    try:
        # 淘宝搜索结果中商品价格通常在 <div class="price g_price g_price-highlight"> 内
        price_div = soup.select_one('div.price.g_price.g_price-highlight')
        if price_div:
            price = price_div.get_text(strip=True)
            return price
        else:
            # 如果没找到，可以尝试找其他价格相关标签，或者返回无价格信息
            return "淘宝价格未找到"
    except Exception as e:
        return f"解析失败: {e}"
