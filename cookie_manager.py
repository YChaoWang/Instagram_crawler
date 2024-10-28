import pickle
import time
import os
from tqdm import tqdm

from scrape import auto_login


class CookieManager:
    def __init__(self, driver, cookie_file="cookies.pkl"):
        self.cookie_file = cookie_file
        self.driver = driver

    def count_cookies(self):
        """Return the current number of cookies in the session and measure time taken"""
        start_time = time.time()
        cookie_count = len(self.driver.get_cookies())
        elapsed_time = time.time() - start_time
        print(f"Time to count cookies: {elapsed_time:.4f} seconds")
        return cookie_count

    def manual_login_and_save(self, username, password):
        """Handle manual login, save new cookies, and measure time taken"""
        try:
            self.driver.get("https://www.instagram.com")
            # print("\nPlease login manually in the browser window...")
            # input("Press Enter after you have successfully logged in...")
            print("\nLogin automatically in the browser window...")
            login_state = auto_login(self.driver, username, password)
            if login_state:
                print("Login successfully")
            else:
                print("Login failed")
            # # Wait with progress bar
            # for _ in tqdm(range(5), desc="Waiting for login processing..."):
            #     time.sleep(1)

            # Save new cookies with timing
            start_time = time.time()
            cookies = self.driver.get_cookies()
            with open(self.cookie_file, "wb") as file:
                pickle.dump(cookies, file)
            elapsed_time = time.time() - start_time
            print(f"New cookies saved successfully to {self.cookie_file}")
            print(f"Time to save cookies: {elapsed_time:.4f} seconds")

        except Exception as e:
            print(f"Error during manual login: {str(e)}")
            raise

    def load_cookies(self):
        """Load and verify saved cookies and measure time taken"""
        try:
            start_time = time.time()
            try:
                with open(self.cookie_file, "rb") as file:
                    cookies = pickle.load(file)
            except FileNotFoundError:
                print(f"Cookie file {self.cookie_file} not found.")
                return False
            except Exception as e:
                print(f"Error loading cookies from file: {str(e)}")
                return False

            self.driver.get("https://www.instagram.com")

            # Add cookies to the session with a progress bar
            for cookie in tqdm(cookies, desc="Adding cookies"):
                if "expiry" in cookie:
                    cookie["expiry"] = int(cookie["expiry"])
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(
                        f"Warning: Could not add cookie {cookie.get('name')}: {str(e)}"
                    )

            self.driver.refresh()
            time.sleep(3)

            if "/login" in self.driver.current_url:
                print("Cookie validation failed - redirected to login page")
                return False

            elapsed_time = time.time() - start_time
            print(f"Time to load cookies: {elapsed_time:.4f} seconds")
            return True

        except Exception as e:
            print(f"Error loading cookies: {str(e)}")
            return False
