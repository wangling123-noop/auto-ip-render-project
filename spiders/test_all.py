from taobao_spider import crawl_taobao_price
from jd_spider import crawl_jd_price
from dangdang_spider import crawl_dangdang_price

book = "python编程"

print("📘 淘宝:", crawl_taobao_price(book))
print("📕 京东:", crawl_jd_price(book))
print("📗 当当:", crawl_dangdang_price(book))
