import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_request(
    url,
    headers=None,
    params=None,
    data=None,
    method="GET",
    timeout=30,
    proxies=None,
    verify=True,
    debug=False
):
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

    # 默认 User-Agent，如果 headers 没有提供
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36"
        }

    try:
        if debug:
            print(f"🚀 发起请求: {url}")
            if proxies:
                print(f"🕵️ 使用代理: {proxies}")
            print(f"📨 请求方式: {method}")

        if method.upper() == "GET":
            response = session.get(url, headers=headers, params=params, timeout=timeout, proxies=proxies, verify=verify)
        elif method.upper() == "POST":
            response = session.post(url, headers=headers, params=params, data=data, timeout=timeout, proxies=proxies, verify=verify)
        else:
            raise ValueError(f"不支持的请求方法: {method}")

        response.raise_for_status()

        if debug:
            print(f"✅ 请求成功，状态码: {response.status_code}")
            print(f"📡 响应内容(前200字): {response.text[:200]}")

        return response

    except requests.exceptions.ProxyError as e:
        print(f"❌ 代理连接失败: {e}")
    except requests.exceptions.Timeout as e:
        print(f"❌ 请求超时: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP错误: {e}")
    except Exception as e:
        print(f"❌ 请求失败: {url}\n原因: {e}")

    return None
