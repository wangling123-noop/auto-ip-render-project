from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

def crawl_jd_price(book_name):
    url = f"https://search.jd.com/Search?keyword={book_name}"

    options = Options()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Edge(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # 等待页面加载完成

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # 京东价格一般在 class="p-price" 的 <i> 标签内
        price_tag = soup.select_one('.p-price i')
        if price_tag:
            price = price_tag.get_text(strip=True)
            return price
        else:
            return "京东价格未找到"

    except Exception as e:
        return f"解析失败: {e}"

    finally:
        driver.quit()
