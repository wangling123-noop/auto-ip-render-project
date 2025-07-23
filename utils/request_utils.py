import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import random

username = "t15324050834262"
password = "6f2j0zgs"
tunnel = "j197.kdltpspro.com:15818"

proxies = {
    "http": f"http://{username}:{password}@{tunnel}/",
    "https": f"http://{username}:{password}@{tunnel}/"
}

USER_AGENTS = [
    # 这里添加多个User-Agent，示例：
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    # 继续添加更多
]

def make_request(
    url,
    headers=None,
    params=None,
    data=None,
    method="GET",
    timeout=30,
    proxies=proxies,
    verify=True,
    debug=False
):
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods={"GET", "POST"},
        raise_on_status=True
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    if headers is None:
        headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        if debug:
            print(f"🚀 请求地址: {url}")
            print(f"📨 请求方式: {method}")
            print(f"🕵️ 代理设置: {proxies if proxies else '未使用'}")

        start_time = time.time()

        if method.upper() == "GET":
            response = session.get(
                url, headers=headers, params=params,
                timeout=timeout, proxies=proxies, verify=verify
            )
        elif method.upper() == "POST":
            response = session.post(
                url, headers=headers, params=params, data=data,
                timeout=timeout, proxies=proxies, verify=verify
            )
        else:
            raise ValueError(f"❌ 不支持的请求方法: {method}")

        elapsed = round(time.time() - start_time, 2)
        response.raise_for_status()

        if debug:
            print(f"✅ 请求成功 | 状态码: {response.status_code} | 耗时: {elapsed}s")
            print(f"📡 响应前200字: {response.text[:200]}")

        return response

    except requests.exceptions.ProxyError as e:
        print(f"❌ 代理连接失败: {e}")
    except requests.exceptions.Timeout as e:
        print(f"⏰ 请求超时: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ HTTP错误: {e} | 状态码: {getattr(e.response, 'status_code', '未知')}")
    except requests.exceptions.RequestException as e:
        print(f"🚫 请求异常: {e}")
    except Exception as e:
        print(f"🔥 其他异常: {e}")

    finally:
        session.close()

    return None
