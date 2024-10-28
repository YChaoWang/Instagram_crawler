from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class WebScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be visible on the page"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None

    def scroll_page(self, scroll_pause_time=2):
        """Scroll the page to load dynamic content"""
        try:
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            while True:
                # Scroll down
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(scroll_pause_time)

                # Calculate new scroll height
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height
            return True
        except Exception as e:
            print(f"Error scrolling page: {str(e)}")
            return False

    def get_instagram_posts(self, username):
        """Scrape Instagram posts for a given username"""
        try:
            # Navigate to user profile
            self.driver.get(f"https://www.instagram.com/{username}/")

            # Wait for posts to load
            posts = self.wait_for_element(By.CSS_SELECTOR, "article img")
            if not posts:
                return []

            # Scroll to load more posts
            self.scroll_page()

            # Get all post URLs
            post_elements = self.driver.find_elements(By.CSS_SELECTOR, "article a")
            post_urls = [elem.get_attribute("href") for elem in post_elements]

            return post_urls

        except Exception as e:
            print(f"Error scraping Instagram posts: {str(e)}")
            return []
