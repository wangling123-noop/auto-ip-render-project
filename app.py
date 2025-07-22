from flask import Flask, request, jsonify
from spiders.taobao_spider import crawl_taobao_price
from spiders.jd_spider import crawl_jd_price
from spiders.dangdang_spider import crawl_dangdang_price
import os

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    data = request.get_json()
    book_name = data.get("book_name")
    if not book_name:
        return jsonify({"error": "书名不能为空"}), 400

    prices = {
        "淘宝": crawl_taobao_price(book_name),
        "京东": crawl_jd_price(book_name),
        "当当": crawl_dangdang_price(book_name),
    }

    return jsonify({
        "book_name": book_name,
        "prices": prices
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
