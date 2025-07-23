from flask import Flask, request, jsonify
from spiders.taobao_spider import crawl_taobao_price
from spiders.jd_spider import crawl_jd_price
from spiders.dangdang_spider import crawl_dangdang_price
import os
import concurrent.futures
import logging
import requests
import socket

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "欢迎使用图书价格查询接口，请访问 /api/price 发送 POST 请求。\n也可以访问 /test_proxy 和 /test_socket 测试代理状态。"

@app.route('/api/price', methods=['POST'])
def get_price():
    if not request.is_json:
        return jsonify({"error": "请求体必须是 JSON 格式"}), 400

    data = request.get_json()

    # 支持批量查询
    if isinstance(data, list):
        if not data:
            return jsonify({"error": "请求体数组为空"}), 400
        results = []
        for item in data:
            res = process_single_query(item)
            results.append(res)
        return jsonify(results)

    elif isinstance(data, dict):
        return jsonify(process_single_query(data))

    else:
        return jsonify({"error": "请求体格式错误，期望对象或数组"}), 400

def process_single_query(data):
    book_name = data.get('book_name')
    if not book_name or not isinstance(book_name, str):
        return {"error": "缺少或无效的书名参数"}

    funcs = [
        (crawl_taobao_price, "淘宝"),
        (crawl_jd_price, "京东"),
        (crawl_dangdang_price, "当当")
    ]

    def safe_crawl(func_tuple):
        func, name = func_tuple
        try:
            result = func(book_name)
            if result is None:
                return (name, f"{name}价格获取失败")
            return (name, result)
        except Exception as e:
            logging.error(f"{name} 爬取异常: {e}")
            return (name, f"{name}价格获取异常: {str(e)}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        crawl_results = executor.map(safe_crawl, funcs)

    prices = {name: res for name, res in crawl_results}
    return {"book_name": book_name, "prices": prices}

# ==== 以下是代理相关测试接口 ====

@app.route("/test_proxy")
def test_proxy():
    proxies = {
        "http": "http://t15324050834262:6f2j0zgs@j197.kdltpspro.com:15818",
        "https": "http://t15324050834262:6f2j0zgs@j197.kdltpspro.com:15818"
    }
    try:
        res = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        return jsonify({
            "success": True,
            "origin_ip": res.json().get("origin"),
            "raw": res.json()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/test_socket")
def test_socket():
    host = "j197.kdltpspro.com"
    port = 15818
    s = socket.socket()
    s.settimeout(5)
    try:
        s.connect((host, port))
        return f"✅ 成功连接到 {host}:{port}"
    except Exception as e:
        return f"❌ 无法连接到 {host}:{port}，错误信息：{e}"
    finally:
        s.close()

# ==== 启动服务 ====
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
