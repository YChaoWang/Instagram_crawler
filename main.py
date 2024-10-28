from firefox_driver import FirefoxDriver
from cookie_manager import CookieManager
from scrape import (
    scrape_instagram_data,
)
import os
import re
import time  # 引入 time 模組
from scrape_post import search_instagram_location
from util.count_post_num import convert_post_count_to_int
from util.save_data import save_to_json


def process_instagram_data(driver, extracted_data):
    if extracted_data:
        # 在處理 Instagram 數據前，先處理 cookie 登入
        cookie_manager = CookieManager(driver)

        if os.path.exists(cookie_manager.cookie_file):
            print("\nFound existing cookies, attempting to load...")
            if not cookie_manager.load_cookies():
                print("Cookies expired or invalid")
                cookie_manager.manual_login_and_save("coffee69_addict", "lovelove6969")
        else:
            print("Need to perform manual login...")
            cookie_manager.manual_login_and_save("coffee69_addict", "lovelove6969")
            cookie_manager.load_cookies()

        # 儲存貼文數量最多的鏈結
        max_posts = 0
        index = -1  # 初始化索引
        max_posts_link = ""

        # 開始處理 Instagram 數據
        for i, data in enumerate(extracted_data):  # 使用 enumerate 獲取索引
            # 提取貼文數量並轉換為整數
            posts_count_str = data[5]  # 假設貼文數量在索引 5
            posts_count_num = convert_post_count_to_int(posts_count_str)

            # 如果當前鏈結的貼文數量更多，則更新 max_posts 和 max_posts_link
            if posts_count_num > max_posts:
                max_posts = posts_count_num
                max_posts_link = data[0]  # 假設鏈結在索引 0
                index = i  # 更新索引

        print(
            f"貼文數量最多的鏈結是: {max_posts_link}，總數量: {max_posts}，索引: {index + 1}"
        )  # 顯示索引（從 1 開始）

        # 進一步搜尋該鏈結的帳號
        print(f"將搜尋 Instagram 帳號: {max_posts_link}")
        post_start_time = time.time()
        post_info = search_instagram_location(driver, max_posts_link, 10)
        post_end_time = time.time()
        cost_time = post_end_time - post_start_time
        print(f"Time to crawl post: {cost_time}")
        cafe_name = extracted_data[i][1]
        post_info = {"cafe name": cafe_name, **post_info}  # 將 cafe name 放在最前面
        # 創建字典以存儲所有信息
        cafe_info = {
            "cafe name": cafe_name,
            "post count": max_posts,  # 貼文數量
        }

        print(f"Cafe Info: {cafe_info}")
        print(f"Cafe Post Info: {post_info}")
        # 將 post_info 存儲為 JSON 文件
        # 將結果字典存儲為 JSON 文件
        save_to_json(
            cafe_info, f"cafe_location_info_{cafe_name}.json"
        )  # 調用新函數保存為 JSON
        save_to_json(post_info, f"post_info_{cafe_name}.json")  # 調用新函數保存為 JSON

    else:
        print("未找到符合條件的 Instagram 地點數據。")


def main():
    start_time = time.time()  # 記錄開始時間
    print("Initialing Firefox driver...")
    # 創建瀏覽器實例
    firefox = FirefoxDriver()
    driver = firefox.start_driver()
    print("Starting the Instagram data scraping process...")

    try:
        # 定義搜尋關鍵字
        search_query = "喜鵲咖啡 ig"
        print(f"搜尋: {search_query}")

        # 定義要提取的索引
        indexes_to_extract = [0, 1, 2, 3, 4, 5, 6]

        # 調用 scrape_instagram_data 函數
        extracted_data = scrape_instagram_data(driver, search_query, indexes_to_extract)

        # 打印結果
        if extracted_data:
            for i, data in enumerate(extracted_data):
                print(f"Instagram 連結 {i + 1} 的數據:")
                for item in data:
                    print(item)
                print("------------------------")
        else:
            print("未找到符合條件的 Instagram 地點數據。")
        find_location = time.time()
        location_stage_time = find_location - start_time
        print(f"總花費時間: {location_stage_time:.2f} 秒")  # 打印總花費時間

        # 處理提取到的 Instagram 數據
        process_instagram_data(driver, extracted_data)
        # input("Enter to close...")

    finally:
        if driver:
            driver.quit()  # 確保在結束時關閉瀏覽器

    end_time = time.time()  # 記錄結束時間
    total_time = end_time - start_time  # 計算總花費時間
    print(f"總花費時間: {total_time:.2f} 秒")  # 打印總花費時間


if __name__ == "__main__":
    main()
