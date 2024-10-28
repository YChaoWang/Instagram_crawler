from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 設定 Chrome 驅動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

search_query = "未央咖啡店 IG 地點"
driver.get(f"https://www.google.com/search?q={search_query}")

# 等待頁面加載
driver.implicitly_wait(10)  # 最多等 10 秒

# 尋找 Instagram 的連結
instagram_links = []
links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    href = link.get_attribute("href")
    if href and "www.instagram.com/explore/locations" in href:
        print(f"找到 Instagram 連結: {href}")
        instagram_links.append(href)

# 提取 Instagram 中的類別名稱和帖子數量
for instagram_link in instagram_links:
    driver.get(instagram_link)

    # 等待頁面加載
    driver.implicitly_wait(10)  # 最多等 10 秒

    try:
        # 等待包含所需信息的 div 元素加載
        spans = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    '//div[contains(@class, "x9f619")]/span[contains(@class, "x1lliihq")]',
                )
            )
        )

        # 提取需要的數據，這裡使用索引
        needed_data = []
        indexes_to_extract = [0, 1, 2, 3, 5]  # 需要提取的索引

        for index in indexes_to_extract:
            if index < len(spans):  # 確保索引不超出範圍
                text = spans[index].text.strip()
                needed_data.append(text)

        # 打印所需的數據
        for item in needed_data:
            print(item)

    except Exception as e:
        print(f"發生錯誤: {e}")

# 等待 10 秒以便查看網頁
input("按 Enter 鍵關閉瀏覽器")
driver.quit()
