from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

def crawl_taobao_price(book_name):
    url = f"https://s.taobao.com/search?q={book_name}"

    options = Options()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Edge(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # 等待页面加载完成

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # 淘宝价格通常在 class="price" 下的 <strong> 或 <span> 标签中
        price_tag = soup.select_one('.price strong, .price span')
        if price_tag:
            price = price_tag.get_text(strip=True)
            return price
        else:
            return "淘宝价格未找到"

    except Exception as e:
        return f"解析失败: {e}"

    finally:
        driver.quit()
