import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from proxy_pool.premium_proxy import get_kuaidaili_proxy

def crawl_jd_price(book_name):
    try:
        url = f"https://search.jd.com/Search?keyword={book_name}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        proxies = get_kuaidaili_proxy()

        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        response = session.get(url, headers=headers, proxies=proxies, timeout=15)
        if response.status_code == 200:
            return "京东价格获取成功（示例）"
        else:
            return f"状态码异常：{response.status_code}"
    except Exception as e:
        return f"请求失败：{e}"
