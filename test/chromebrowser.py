from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_browser():
    """創建並返回一個 Chrome 瀏覽器實例"""
    opt = webdriver.ChromeOptions()
    opt.add_argument("--headless")  # 啟用 headless 模式
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opt
    )
    return driver
