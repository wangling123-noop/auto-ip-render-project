from flask import Flask, request, jsonify
from spiders.taobao_spider import crawl_taobao_price
from spiders.jd_spider import crawl_jd_price
from spiders.dangdang_spider import crawl_dangdang_price
import os

app = Flask(__name__)

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
