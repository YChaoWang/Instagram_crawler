import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm
import time
import concurrent.futures


def tqdm_wait(driver, timeout, condition, desc="Waiting"):
    """Use tqdm to show wait time for WebDriverWait."""
    with tqdm(total=timeout, desc=desc, unit="s") as pbar:
        for i in range(timeout):
            try:
                WebDriverWait(driver, 1).until(condition)
                break
            except TimeoutException:
                time.sleep(1)
                pbar.update(1)
        else:
            raise TimeoutException(f"Timeout while waiting for condition: {desc}")


def scrape_instagram_data(driver, search_query, indexes_to_extract=[0, 1, 2, 3, 5]):
    driver.get(f"https://www.google.com/search?q={search_query}")
    time.sleep(np.random.uniform(3, 5))

    tqdm_wait(
        driver,
        20,
        EC.presence_of_element_located((By.TAG_NAME, "a")),
        desc="Loading Google Search Page",
    )

    # Collect Instagram links first
    instagram_links = []
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and "www.instagram.com/explore/locations" in href:
            instagram_links.append(href)
            print("Instagram location 連結:", href)

    # If no links are found, exit the function
    if not instagram_links:
        print("未找到 Instagram 地點連結")
        return []

    # Use ThreadPoolExecutor to scrape Instagram links concurrently after all links have been gathered
    all_needed_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Only start executing scrape_individual_location after all links are collected
        future_to_link = {
            executor.submit(
                scrape_individual_location, driver, link, indexes_to_extract
            ): link
            for link in instagram_links
        }
        for future in concurrent.futures.as_completed(future_to_link):
            try:
                data = future.result()
                if data:
                    all_needed_data.append(data)
            except Exception as e:
                print(f"Error scraping {future_to_link[future]}: {e}")

    return all_needed_data


def scrape_individual_location(driver, instagram_link, indexes_to_extract):
    # Ensure instagram_link is a string
    if not isinstance(instagram_link, str):
        raise ValueError(f"Expected a string URL, got {type(instagram_link)}")

    driver.get(instagram_link)
    time.sleep(np.random.uniform(3, 5))
    # Extract the required data
    needed_data = []
    needed_data.append(instagram_link)
    # 等待包含 x9f619 的 div 加載完成
    try:
        tqdm_wait(
            driver,
            10,
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "x9f619")]//h1')
            ),
            desc="Loading Instagram Location Page",
        )
    except TimeoutException:
        print("Timeout: 無法找到指定元素，請檢查 XPath 或增加等待時間。")

    # 抓取 h1 的內容
    location_title = None
    try:
        location_title_element = driver.find_element(By.XPATH, "//h1")
        location_title = location_title_element.text.strip()
        print("地點標題:", location_title)
    except Exception as e:
        print("無法找到地點標題:", e)

    # Wait for the required elements to load
    try:
        tqdm_wait(
            driver,
            20,
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    '//div[contains(@class, "x9f619")]/span[contains(@class, "x1lliihq")]',
                )
            ),
            desc="Loading Instagram Location Page",
        )
    except TimeoutException:
        print("Timeout: 無法找到指定元素，請檢查 XPath 或增加等待時間。")
        return None

    needed_data.append(location_title)
    spans = driver.find_elements(
        By.XPATH, '//div[contains(@class, "x9f619")]/span[contains(@class, "x1lliihq")]'
    )
    for index in indexes_to_extract:
        if index < len(spans):
            needed_data.append(spans[index].text.strip())

    # # 把地點標題和鏈結加入到數據
    # all_needed_data.append([instagram_link] + [location_title] + needed_data)
    # print(f"Needed data: {needed_data}\n")

    return needed_data


def search_instagram_profile(driver, search_query):
    profile_url = f"https://www.google.com/search?q={search_query}"
    driver.get(profile_url)
    time.sleep(np.random.uniform(3, 5))

    tqdm_wait(
        driver,
        20,
        EC.presence_of_element_located((By.TAG_NAME, "a")),
        desc="Loading Google Search Page",
    )

    instagram_profile_links = []
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        href = link.get_attribute("href")
        # print("link:", href)
    if href:
        href = href.strip()
        print("href:", href)
        if "www.instagram.com/" in href:
            print("Instagram profile pure連結:", href)
            # 排除 explore 和 /p/ 相關連結
            if "www.instagram.com/explore/" not in href and "/p/" not in href:
                # 移除 URL 參數，保留格式簡單的連結
                clean_link = href.split("?")[0]
                # print("href:" + href)
                if clean_link not in instagram_profile_links:
                    instagram_profile_links.append(clean_link)
                    print("Instagram profile 連結:", clean_link)
            else:
                print("href 不是 Instagram profile 連結")
        else:
            print("href 未找到 Instagram profile 連結")
            return []
    else:
        print("href 未找到 Instagram profile 連結")
        return []
    if not instagram_profile_links:
        print("未找到 Instagram profile 連結")
        return []

    # 提取指定的數據
    all_needed_profile_data = []
    for instagram_profile_link in instagram_profile_links:
        driver.get(instagram_profile_link)
        input("按 Enter 鍵繼續...")

    try:

        tqdm_wait(
            driver,
            20,
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "x9f619")]')
            ),
            desc="Loading Instagram Profile Page",
        )
    except TimeoutException:
        print("Timeout: 無法找到指定元素，請檢查 XPath 或增加等待時間。")

    numbers = []
    try:
        profile_data = driver.find_elements(
            By.XPATH,
            '//ul[contains(@class, "x78zum5")]/li//span[contains(@class, "x5n08af")]',
        )
        for data in profile_data:
            text = data.text.strip()
            try:
                number = int(text.replace(",", "").split()[0])
                numbers.append(number)
            except ValueError:
                continue

        print("抓取到的數字:", numbers)

    except Exception as e:
        print(f"發生錯誤: {e}")

    return numbers


def auto_login(driver, username, password):
    try:
        tqdm_wait(
            driver,
            20,
            EC.presence_of_all_elements_located((By.TAG_NAME, "input")),
            desc="Loading Instagram Login Page",
        )

        # 找到所有的 input 元素
        input_elements = driver.find_elements(By.TAG_NAME, "input")

        try:
            # 遍歷每個 input 元素
            for input_element in input_elements:
                # 檢查 name 屬性是否為 "username"
                if input_element.get_attribute("name") == "username":
                    # 填入指定的值
                    input_value = username  # 請替換為實際要填入的值
                    input_element.send_keys(input_value)
                    print("已成功填入username。")
                elif input_element.get_attribute("name") == "password":
                    # 填入指定的值
                    input_value = password
                    input_element.send_keys(input_value)
                    print("已成功填入password。")
                else:
                    break  # 假設只需填一個，填完即退出循環
        except Exception as e:
            print(f"填入值時出現錯誤: {e}")

        try:
            tqdm_wait(
                driver,
                20,
                EC.presence_of_all_elements_located((By.TAG_NAME, "button")),
                desc="Submitting Instagram Login Info",
            )

            # 找到所有的 button 元素
            button_elements = driver.find_elements(By.TAG_NAME, "button")
            # 遍歷每個 button 元素
            for button_element in button_elements:
                # 檢查文本是否包含 "Log In" 或者 type 屬性是否為 "submit"
                if button_element.get_attribute("type") == "submit":
                    # 點擊該按鈕
                    button_element.click()
                    print("已成功點擊按鈕。")
                    break  # 點擊完即退出循環
            try:
                tqdm_wait(
                    driver,
                    20,
                    EC.presence_of_element_located((By.XPATH, "//button")),
                    desc="Saving Instagram Login Info",
                )
                # 找到所有的 button 元素
                save_button_element = driver.find_element(By.XPATH, "//button")
                save_button_element.click()
                print("已成功點擊儲存登入資料按鈕。")
            except TimeoutException:
                print(f"Timeout: 無法找到指定元素，請檢查 XPath 或增加等待時間。")
                return False
            # input("Enter to continue...")
        except Exception as e:
            print(f"點擊登入按鈕時出現錯誤: {e}")
        return True

    except TimeoutException as e:
        print(f"Timeout: 無法找到指定元素，請檢查 XPath 或增加等待時間。")
        return False
