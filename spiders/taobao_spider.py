from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import traceback
import time

# 快代理配置
username = "t15324050834262"
password = "6f2j0zgs"
tunnel = "j197.kdltpspro.com:15818"

# 伪装浏览器 User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
]

def get_edge_driver_with_proxy_and_ua():
    options = Options()
    options.use_chromium = True
    options.add_argument("--headless=new")  # 使用新的 headless 模式，提升兼容性
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 设置随机 User-Agent
    ua = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={ua}")

    # 设置代理
    proxy_str = f"http://{username}:{password}@{tunnel}"
    options.add_argument(f"--proxy-server={proxy_str}")

    # 初始化 WebDriver
    return webdriver.Edge(options=options)

def crawl_taobao_price(keyword):
    url = f"https://s.taobao.com/search?q={keyword}"
    driver = get_edge_driver_with_proxy_and_ua()
    try:
        driver.set_page_load_timeout(20)
        driver.get(url)

        # 等待商品主区域加载
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".items .item"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # 获取第一个商品价格（适配常见选择器）
        price_span = soup.select_one(".items .price")
        if price_span:
            price = price_span.get_text(strip=True)
            time.sleep(random.uniform(1.2, 2.5))  # 延迟，防止封锁
            return f"{price} 元"
        else:
            return "淘宝价格未找到"

    except Exception as e:
        return f"❌ 解析失败: {str(e)}\n{traceback.format_exc()}"
    finally:
        driver.quit()

if __name__ == "__main__":
    book = "python编程"
    print(f"淘宝价格: {crawl_taobao_price(book)}")
