from firefox_driver import FirefoxDriver
from cookie_manager import CookieManager
from scrape import scrape_instagram_data
import os
import re
import time
import argparse
from scrape_post import search_instagram_location
from util.count_post_num import convert_post_count_to_int
from util.save_data import save_to_json


def process_instagram_data(driver, extracted_data, username, password):
    if extracted_data:
        cookie_manager = CookieManager(driver)

        if os.path.exists(cookie_manager.cookie_file):
            print("\nFound existing cookies, attempting to load...")
            if not cookie_manager.load_cookies():
                print("Cookies expired or invalid")
                cookie_manager.manual_login_and_save(username, password)
        else:
            print("Need to perform manual login...")
            cookie_manager.manual_login_and_save(username, password)
            cookie_manager.load_cookies()

        max_posts = 0
        index = -1
        max_posts_link = ""

        for i, data in enumerate(extracted_data):
            posts_count_str = data[5]
            posts_count_num = convert_post_count_to_int(posts_count_str)

            if posts_count_num > max_posts:
                max_posts = posts_count_num
                max_posts_link = data[0]
                index = i

        print(
            f"貼文數量最多的鏈結是: {max_posts_link}，總數量: {max_posts}，索引: {index + 1}"
        )

        print(f"將搜尋 Instagram 帳號: {max_posts_link}")
        post_start_time = time.time()
        post_info = search_instagram_location(driver, max_posts_link, 10)
        post_end_time = time.time()
        cost_time = post_end_time - post_start_time
        print(f"Time to crawl post: {cost_time}")

        cafe_name = extracted_data[i][1]
        post_info = {"cafe name": cafe_name, **post_info}

        cafe_info = {
            "cafe name": cafe_name,
            "post count": max_posts,
        }

        print(f"Cafe Info: {cafe_info}")
        print(f"Cafe Post Info: {post_info}")

        save_to_json(cafe_info, f"cafe_location_info_{cafe_name}.json")
        save_to_json(post_info, f"post_info_{cafe_name}.json")

    else:
        print("未找到符合條件的 Instagram 地點數據。")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Instagram Scraper with customizable settings"
    )

    # Required arguments
    parser.add_argument("-u", "--username", required=True, help="Instagram username")
    parser.add_argument("-p", "--password", required=True, help="Instagram password")

    # Optional arguments with defaults
    parser.add_argument(
        "-q",
        "--query",
        default="喜鵲咖啡 ig",
        help='Search query (default: "喜鵲咖啡 ig")',
    )
    parser.add_argument(
        "-i",
        "--indexes",
        default=[0, 1, 2, 3, 4, 5, 6],
        type=int,
        nargs="+",
        help="Indexes to extract (default: 0 1 2 3 4 5 6)",
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()
    start_time = time.time()

    print("Initialing Firefox driver...")
    firefox = FirefoxDriver()
    driver = firefox.start_driver()
    print("Starting the Instagram data scraping process...")

    try:
        print(f"搜尋: {args.query}")
        extracted_data = scrape_instagram_data(driver, args.query, args.indexes)

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
        print(f"總花費時間: {location_stage_time:.2f} 秒")

        process_instagram_data(driver, extracted_data, args.username, args.password)

    finally:
        if driver:
            driver.quit()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"總花費時間: {total_time:.2f} 秒")


if __name__ == "__main__":
    main()
