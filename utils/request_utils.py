# utils/request_utils.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_request(url, headers=None, params=None, timeout=30, proxies=None):
    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(
            url,
            headers=headers,
            params=params,
            timeout=timeout,
            proxies=proxies  # ✅ 在这里传入代理
        )
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"❌ 请求失败: {url}\n原因: {e}")
        return None
