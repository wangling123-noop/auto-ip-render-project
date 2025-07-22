def get_kuaidaili_proxy():
    username = "t15318226940336"
    password = "xwalb2ql"
    proxy_host = "z579.kdltps.com"
    proxy_port = "15818"

    proxy_meta = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
    return {
        "http": proxy_meta,
        "https": proxy_meta,
    }
