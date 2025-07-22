from flask import Flask, request, jsonify
from spiders.taobao_spider import crawl_taobao_price
from spiders.jd_spider import crawl_jd_price
from spiders.dangdang_spider import crawl_dangdang_price
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

app = Flask(__name__)

# 通用请求函数：用于爬虫内部统一调用
def make_request(url, headers=None, params=None, timeout=30):
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
        response = session.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"❌ 请求失败: {url}\n原因: {e}")
        return None

@app.route('/')
def index():
    return "欢迎使用图书价格查询接口，请访问 /api/price 发送 POST 请求"

@app.route('/api/price', methods=['POST'])
def get_price():
    data = request.get_json()

    # 如果是数组，取第一个元素
    if isinstance(data, list):
        if not data:
            return jsonify({"error": "请求体数组为空"}), 400
        data = data[0]

    if not isinstance(data, dict):
        return jsonify({"error": "请求体格式错误，期望对象或数组"}), 400

    book_name = data.get('book_name')
    if not book_name:
        return jsonify({"error": "缺少书名参数"}), 400

    return jsonify({
        "book_name": book_name,
        "prices": {
            "淘宝": crawl_taobao_price(book_name),
            "京东": crawl_jd_price(book_name),
            "当当": crawl_dangdang_price(book_name)
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
