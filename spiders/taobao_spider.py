from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import traceback
import time

username = "t15324050834262"
password = "6f2j0zgs"
tunnel = "j197.kdltpspro.com:15818"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
]

def get_edge_driver_with_proxy_and_ua():
    options = Options()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    ua = random.choice(USER_AGENTS)
    options.add_argument(f'user-agent={ua}')

    proxy_str = f"http://{username}:{password}@{tunnel}"
    options.add_argument(f'--proxy-server={proxy_str}')

    driver = webdriver.Edge(options=options)
    return driver

def crawl_taobao_price(keyword):
    url = f"https://s.taobao.com/search?q={keyword}"
    driver = get_edge_driver_with_proxy_and_ua()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.price, .J_price'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        price_span = soup.select_one('.price, .J_price')
        if price_span:
            time.sleep(random.uniform(1, 3))  # 防封锁，稍微延迟
            return price_span.get_text(strip=True)
        else:
            return "淘宝价格未找到"
    except Exception as e:
        error_msg = traceback.format_exc()
        return f"解析失败: {e}\n{error_msg}"
    finally:
        driver.quit()

if __name__ == "__main__":
    book = "python编程"
    print(f"淘宝价格: {crawl_taobao_price(book)}")
