import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import random

# 快代理配置
username = "t15324050834262"
password = "6f2j0zgs"
tunnel = "j197.kdltpspro.com:15818"

# 代理隧道列表，可扩展
PROXY_TUNNELS = [
    {"host": "j197.kdltpspro.com", "port": 15818},
    # {"host": "j198.kdltpspro.com", "port": 15818},  # 如有更多可加
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]

def get_session_with_retries():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods={"GET", "POST"},
        raise_on_status=True
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=1, pool_maxsize=1, pool_block=False)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def rotate_proxy():
    tunnel = random.choice(PROXY_TUNNELS)
    proxy = {
        "http": f"http://{username}:{password}@{tunnel['host']}:{tunnel['port']}",
        "https": f"http://{username}:{password}@{tunnel['host']}:{tunnel['port']}"
    }
    print(f"[代理轮换] 当前使用代理: {proxy}")
    return proxy

def make_request(url, method="GET", headers=None, params=None, data=None, timeout=30, proxies=None, verify=True, debug=True):
    session = get_session_with_retries()
    if headers is None:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Connection": "close",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate"
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

        return response
    except requests.exceptions.ProxyError as e:
        print(f"❌ 代理连接失败: {e}")
        time.sleep(5)
    except requests.exceptions.Timeout as e:
        print(f"⏰ 请求超时: {e}")
    except requests.exceptions.HTTPError as e:
        status_code = getattr(e.response, 'status_code', '未知')
        print(f"⚠️ HTTP错误: {e} | 状态码: {status_code}")
        if status_code == 407:
            print("⚠️ 代理认证失败，请检查用户名和密码是否正确")
    except requests.exceptions.RequestException as e:
        print(f"🚫 请求异常: {e}")
    except Exception as e:
        print(f"🔥 其他异常: {e}")
    finally:
        session.close()
    return None

def get_current_ip(proxies, debug=True):
    url = "http://httpbin.org/ip"
    response = make_request(url, proxies=proxies, debug=debug)
    if response:
        try:
            ip_info = response.json()
            ip = ip_info.get("origin", "未知IP")
            if debug:
                print(f"[当前代理IP] {ip}")
            return ip
        except Exception as e:
            print(f"解析IP失败: {e}")
            return "解析IP失败"
    return "无法获取IP"

if __name__ == "__main__":
    for i in range(5):
        print(f"\n=== 第{i+1}次请求 ===")
        proxies = rotate_proxy()
        current_ip = get_current_ip(proxies)
        print(f"当前代理出口IP: {current_ip}")

        if current_ip in ["无法获取IP", "解析IP失败"]:
            print("⚠️ 代理可能未正确配置，请检查代理信息")
        
        target_url = "https://httpbin.org/get"
        response = make_request(target_url, proxies=proxies)
        if response:
            print(f"目标网站响应状态码: {response.status_code}")
        else:
            print("请求目标网站失败")

        wait_time = random.uniform(3, 7)
        print(f"等待{wait_time:.1f}秒后尝试下一次请求...")
        time.sleep(wait_time)
