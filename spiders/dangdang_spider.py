from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random

username = "t15324050834262"
password = "6f2j0zgs"
tunnel = "j197.kdltpspro.com:15818"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    # 你可以添加更多User-Agent
]

def get_edge_driver_with_proxy_and_ua():
    options = Options()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # 随机User-Agent
    ua = random.choice(USER_AGENTS)
    options.add_argument(f'user-agent={ua}')

    proxy_str = f"http://{username}:{password}@{tunnel}"
    options.add_argument(f'--proxy-server={proxy_str}')

    driver = webdriver.Edge(options=options)
    return driver

def get_current_ip():
    driver = get_edge_driver_with_proxy_and_ua()
    try:
        driver.get("http://httpbin.org/ip")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        ip_text = driver.find_element(By.TAG_NAME, "pre").text
        return ip_text
    finally:
        driver.quit()

def crawl_dangdang_price(book_name):
    url = f"http://search.dangdang.com/?key={book_name}&act=input"
    driver = get_edge_driver_with_proxy_and_ua()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.price span'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        price_span = soup.select_one('p.price span')
        if price_span:
            return price_span.get_text(strip=True)
        else:
            return "当当价格未找到"
    except Exception as e:
        return f"解析失败: {e}"
    finally:
        driver.quit()

if __name__ == "__main__":
    print("当前代理IP:", get_current_ip())
    book = "python编程"
    price = crawl_dangdang_price(book)
    print(f"书名《{book}》的价格是：{price}")
