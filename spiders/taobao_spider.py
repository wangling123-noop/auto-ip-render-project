from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import traceback
import time
import logging

# 启用日志（可选）
logging.basicConfig(level=logging.INFO)

username = "t15332794831619"
password = "78wssuy2"
tunnel = "p385.kdltps.com:15818"
driver_path = r"D:\2025723\edgedriver_win64\msedgedriver.exe"

# User-Agent 池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
]

def get_driver():
    # ✅ 显式创建 EdgeDriver 服务对象
    service = Service(executable_path=driver_path)

    options = Options()
    options.use_chromium = True
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 添加随机 User-Agent
    ua = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={ua}")

    # ✅ 使用代理（如不需要代理，可注释下一行）
    proxy_str = f"http://{username}:{password}@{tunnel}"
    options.add_argument(f"--proxy-server={proxy_str}")

    # ✅ 显式传入 service 和 options（关键）
    return webdriver.Edge(service=service, options=options)

def crawl_taobao_price(keyword):
    url = f"https://s.taobao.com/search?q={keyword}"
    driver = get_driver()
    try:
        driver.set_page_load_timeout(20)
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".items .item"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        price_span = soup.select_one(".items .price")
        if price_span:
            price = price_span.get_text(strip=True)
            time.sleep(random.uniform(1.2, 2.5))
            return f"{price} 元"
        else:
            return "淘宝价格未找到"

    except Exception as e:
        return f"❌ 解析失败: {str(e)}\n{traceback.format_exc()}"
    finally:
        driver.quit()

if __name__ == "__main__":
    book = "python编程"
    result = crawl_taobao_price(book)
    try:
        print(f"✅ 淘宝价格: {result}")
    except UnicodeEncodeError:
        print("淘宝价格:", result.encode("utf-8", errors="replace").decode("utf-8"))
