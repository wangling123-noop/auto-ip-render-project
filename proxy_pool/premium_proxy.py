def get_kuaidaili_proxy():
    username = "t15324050834262"
    password = "6f2j0zgs"
    proxy_host = "z579.kdltps.com"
    proxy_port = "15818"

    proxy_meta = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
    return {
        "http": proxy_meta,
        "https": proxy_meta,
    }
