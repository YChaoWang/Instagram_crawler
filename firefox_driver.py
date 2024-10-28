from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
from fake_useragent import UserAgent


class FirefoxDriver:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("--private")  # 無痕模式
        self.driver = None
        self.user_agent = UserAgent().random  # 隨機生成用戶代理

    def start_driver(self):
        """Initialize and start Firefox WebDriver"""
        try:
            start_time = time.time()
            self.options.set_preference(
                "general.useragent.override", self.user_agent
            )  # 設置用戶代理
            self.driver = webdriver.Firefox(options=self.options)
            init_time = time.time() - start_time
            print(f"Time to initialize WebDriver: {init_time:.4f} seconds")
            print(f"Using User Agent: {self.user_agent}")  # 打印使用的用戶代理
            return self.driver
        except Exception as e:
            print(f"Error initializing WebDriver: {str(e)}")
            return None

    def close_driver(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

    def get_page(self, url):
        """Navigate to a specified URL and measure load time"""
        try:
            start_time = time.time()
            self.driver.get(url)
            load_time = time.time() - start_time
            print(f"Time to load page: {load_time:.4f} seconds")
            return True
        except Exception as e:
            print(f"Error loading page: {str(e)}")
            return False
