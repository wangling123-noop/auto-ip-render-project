from flask import Flask, request, jsonify
from spiders.taobao_spider import crawl_taobao_price
from spiders.jd_spider import crawl_jd_price
from spiders.dangdang_spider import crawl_dangdang_price
import os
import concurrent.futures

app = Flask(__name__)

@app.route('/')
def index():
    return "欢迎使用图书价格查询接口，请访问 /api/price 发送 POST 请求"

@app.route('/api/price', methods=['POST'])
def get_price():
    if not request.is_json:
        return jsonify({"error": "请求体必须是 JSON 格式"}), 400

    data = request.get_json()

    if isinstance(data, list):
        if not data:
            return jsonify({"error": "请求体数组为空"}), 400
        data = data[0]

    if not isinstance(data, dict):
        return jsonify({"error": "请求体格式错误，期望对象或数组"}), 400

    book_name = data.get('book_name')
    if not book_name:
        return jsonify({"error": "缺少书名参数"}), 400

    def safe_crawl(func, name):
        try:
            result = func(book_name)
            if result is None:
                return f"{name}价格获取失败"
            return result
        except Exception as e:
            return f"{name}价格获取异常: {str(e)}"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_taobao = executor.submit(safe_crawl, crawl_taobao_price, "淘宝")
        future_jd = executor.submit(safe_crawl, crawl_jd_price, "京东")
        future_dd = executor.submit(safe_crawl, crawl_dangdang_price, "当当")

        prices = {
            "淘宝": future_taobao.result(),
            "京东": future_jd.result(),
            "当当": future_dd.result()
        }

    return jsonify({
        "book_name": book_name,
        "prices": prices
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
