def get_kuaidaili_proxy():
    username = "t15324050834262"
    password = "6f2j0zgs"
    proxy_host = "j197.kdltpspro.com"
    proxy_port = "15818"

    proxy_meta = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
    return {
        "http": proxy_meta,
        "https": proxy_meta,
    }
# 主测试逻辑
if __name__ == "__main__":
    for i in range(5):
        try:
            proxies = get_kuaidaili_proxy()
            resp = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=8)
            print(f"[{i+1}] 当前代理 IP：{resp.json()['origin']}")
        except Exception as e:
            print(f"[{i+1}] 请求失败：{e}")