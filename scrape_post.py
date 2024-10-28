import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from scrape import tqdm_wait


def search_instagram_location(driver, link, target_posts):
    print(f"Search Location Link: {link}")
    driver.get(link)
    time.sleep(np.random.uniform(3, 5))
    # input("Enter to continue...")
    try:
        tqdm_wait(
            driver,
            20,
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "xzboxd6")]//img')
            ),
            desc="Loading Instagram Location Page",
        )
        try:
            # 定位到圖片元素
            image_element = driver.find_element(
                By.XPATH, '//div[contains(@class, "xzboxd6")]//img'
            )

            # 獲取圖片的 src 屬性
            image_src = image_element.get_attribute("src")
            print(f"圖片的 src 屬性為: {image_src}")

            # 模擬點擊動作
            action = ActionChains(driver)
            action.move_to_element(image_element).click().perform()

            print("已點擊圖片元素。")

            # 初始化 post_info 字典
            post_info = {}
            total_posts = 0  # 計數器
            target_posts = target_posts  # 目標貼文數量

            while total_posts < target_posts:
                # 解析貼文中的資料
                post_info_batch = extract_posts_info(
                    driver, total_posts + 1
                )  # 傳遞當前的貼文數量
                post_info.update(post_info_batch)  # 更新 post_info 字典
                total_posts = len(post_info)  # 更新當前貼文數量

                print(f"當前已提取貼文數量: {total_posts}")

                if total_posts < target_posts:
                    click_next_button(driver)  # 點擊下一步按鈕
                    time.sleep(np.random.uniform(2, 4))  # 等待一段時間以便加載新貼文
                else:
                    print("已達到目標貼文數量。")
                    break

            print(f"最終提取的貼文信息: {post_info}")
            return post_info

        except Exception as e:
            print(f"無法點擊圖片: {e}")

    except TimeoutException:
        print("Timeout: 無法找到指定元素，請檢查 XPath 或增加等待時間。")


def extract_posts_info(driver, post_count):
    """提取貼文信息並返回字典"""
    post_info = {}  # 初始化字典以存儲貼文信息
    try:
        post_author_link, author_account_name = get_post_author(
            driver
        )  # 獲取作者的 href 和帳號名稱
        if post_author_link and author_account_name:
            post_info[post_count] = {  # 使用 post_count 作為
                "author": author_account_name,  # 將作者帳號名稱添加到字典
            }
            print("ok")
    except TimeoutException:
        print("Timeout: 無法找到post author")

    try:
        formatted_date = get_post_time_created(driver)  # 調用新函數
        if formatted_date:
            post_info[post_count][
                "created date"
            ] = formatted_date  # 將日期信息添加到字典
            print(f"成功獲取的日期: {formatted_date}")
    except TimeoutException:
        print("Timeout: 無法找到post created time")

    try:
        all_content = get_post_content(driver)
        if all_content:
            post_info[post_count]["content"] = all_content  # 將內容信息添加到字典
            print(f"成功獲取")
    except TimeoutException:
        print("Timeout: 無法找到 post content")

    return post_info  # 返回包含所有信息的字典


def get_post_author(driver):
    """獲取貼文作者的 href"""
    try:
        # 等待作者鏈接元素加載
        tqdm_wait(
            driver,
            20,
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(@class, "xt0psk2")]//a')
            ),
            desc="Loading post author link",
        )
        # 定位到作者鏈接元素
        author_element = driver.find_element(
            By.XPATH, '(//span[contains(@class, "xt0psk2")]//a)[1]'
        )
        # 獲取 href 屬性
        author_href = author_element.get_attribute("href")
        author_account_name = author_href.split("/")[-2]  # 提取用戶名
        print(f"作者的 href 屬性為: {author_href}")
        return author_href, author_account_name  # 返回 href和 author_account_name

    except Exception as e:
        print(f"無法獲取作者的 href: {e}")
        return None  # 返回 None 以表示失敗


def get_post_time_created(driver):
    """獲取貼文創建時間並返回格式化的日期"""
    tqdm_wait(
        driver,
        20,
        EC.presence_of_element_located(
            (By.XPATH, '//time[contains(@class, "x1p4m5qa")] ')
        ),
        desc="Loading post created time",
    )
    try:
        # 定位到post time created
        post_time_created = driver.find_element(
            By.XPATH, '//time[contains(@class, "x1p4m5qa")]'
        )
        print(f"post time created: {post_time_created}")
        # 抓取 datetime 屬性的值
        datetime_str = post_time_created.get_attribute("datetime")
        print(f"原始 datetime 值: {datetime_str}")
        try:
            # 將 datetime 值轉換為 YYYY/MM/DD 格式
            date_obj = datetime.datetime.strptime(
                datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ"
            )  # 使用 strptime 解析
            formatted_date = date_obj.strftime("%Y/%m/%d")  # 轉換格式
            print(f"轉換後的日期: {formatted_date}")
            return formatted_date  # 返回格式化的日期
        except Exception as e:
            print(f"無法轉換原始 datetime 值: {e}")
            return None  # 返回 None 以表示失敗

    except Exception as e:
        print(f"無法解析: {e}")
        return None  # 返回 None 以表示失敗


def get_post_content(driver):
    """提取貼文內容，包括 <br> 和 <a> 標籤的文本"""
    try:
        # 等待 h1 元素加載
        tqdm_wait(
            driver,
            20,
            EC.presence_of_element_located((By.XPATH, "//h1")),
            desc="Loading post content",
        )

        # 獲取 h1 元素
        h1_element = driver.find_element(By.XPATH, "//h1")

        # 取得 h1 的 HTML 內容，並解析所有 <br> 標籤
        html_content = h1_element.get_attribute("innerHTML")

        # 使用 BeautifulSoup 處理 HTML 並替換 <br> 標籤
        soup = BeautifulSoup(html_content, "html.parser")
        text_with_newlines = soup.get_text(separator="\n")  # <br> 變成換行符

        # 將內容拆分成每一行
        parsed_lines = text_with_newlines.strip().split("\n")

        # 打印和返回解析後的行
        print("提取的文本行:", parsed_lines)
        return parsed_lines

    except TimeoutException:
        print("Timeout: 無法找到 h1 元素")
    except Exception as e:
        print(f"發生錯誤: {e}")


def click_next_button(driver):

    try:
        tqdm_wait(
            driver,
            20,
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'_aaqg')]/button[contains(@class, '_abl-')]",
                )
            ),
            desc="Loading next button",
        )

        next_button = driver.find_element(
            By.XPATH,
            "//div[contains(@class,'_aaqg')]/button[contains(@class, '_abl-')]",
        )

        # 模擬點擊動作
        try:
            action = ActionChains(driver)
            action.move_to_element(next_button).click().perform()

            print("已成功點擊下一步按鈕。")
        except Exception as e:
            print(f"點擊失敗: {e}")

    except Exception as e:
        print(f"無法獲取next button: {e}")
