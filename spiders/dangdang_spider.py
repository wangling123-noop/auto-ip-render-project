from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def crawl_dangdang_price(book_name):
    url = f"http://search.dangdang.com/?key={book_name}&act=input"

    options = Options()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Edge(options=options)

    try:
        driver.get(url)

        # 等待价格元素加载，最长10秒
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.price span'))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        price_span = soup.select_one('p.price span')
        if price_span:
            price = price_span.get_text(strip=True)
            return price
        else:
            return "当当价格未找到"

    except Exception as e:
        return f"解析失败: {e}"

    finally:
        driver.quit()
