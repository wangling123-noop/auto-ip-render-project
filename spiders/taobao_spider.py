import requests
from proxy_pool.premium_proxy import get_kuaidaili_proxy

def crawl_taobao_price(book_name):
    try:
        url = f"https://s.taobao.com/search?q={book_name}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        proxies = get_kuaidaili_proxy()
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return "淘宝价格获取成功（示例）"
        else:
            return f"状态码异常：{response.status_code}"
    except Exception as e:
        return f"请求失败：{e}"
