import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import random

username = "t15324050834262"
password = "6f2j0zgs"
tunnel = "j197.kdltpspro.com:15818"

proxies_template = {
    "http": f"http://{username}:{password}@{tunnel}/",
    "https": f"http://{username}:{password}@{tunnel}/"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    # 你可以继续添加更多User-Agent
]

def get_session_with_retries():
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
    return session

def make_request(url, method="GET", headers=None, params=None, data=None, timeout=30, proxies=None, verify=True, debug=False):
    session = get_session_with_retries()

    if headers is None:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Connection": "close"
        }
    else:
        headers.setdefault("Connection", "close")

    try:
        if debug:
            print(f"🚀 请求地址: {url}")
            print(f"📨 请求方式: {method}")
            print(f"🕵️ 代理设置: {proxies if proxies else '未使用'}")
            print(f"👤 User-Agent: {headers['User-Agent']}")

        start_time = time.time()

        if method.upper() == "GET":
            response = session.get(url, headers=headers, params=params, timeout=timeout, proxies=proxies, verify=verify)
        elif method.upper() == "POST":
            response = session.post(url, headers=headers, params=params, data=data, timeout=timeout, proxies=proxies, verify=verify)
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

def get_current_ip(proxies, debug=False):
    url = "http://httpbin.org/ip"
    response = make_request(url, proxies=proxies, debug=debug)
    if response:
        ip_info = response.json()
        return ip_info.get("origin", "未知IP")
    return "无法获取IP"

if __name__ == "__main__":
    for i in range(5):
        print(f"\n=== 第{i+1}次请求 ===")
        proxies = proxies_template  # 如果有多个隧道，可以改这里实现轮换
        current_ip = get_current_ip(proxies, debug=True)
        print(f"当前代理出口IP: {current_ip}")

        target_url = "https://httpbin.org/get"
        response = make_request(target_url, proxies=proxies, debug=True)
        if response:
            print(f"目标网站响应状态码: {response.status_code}")
        else:
            print("请求目标网站失败")

        print("等待5秒后尝试下一次请求...")
        time.sleep(5)
