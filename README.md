# Instagram Crawler

## Overview
This project is an Instagram crawler that allows users to scrape data from Instagram locations and posts. It utilizes Selenium for web automation and BeautifulSoup for HTML parsing. The crawler can extract information such as post counts, authors, and content from specified Instagram locations.

## Features
- Scrapes Instagram location data based on search queries.
- Extracts post information including author, creation date, and content.
- Saves the extracted data in JSON format.
- Supports cookie management for login persistence.

## Requirements
- Python 3.x
- Selenium
- BeautifulSoup4
- WebDriver Manager
- Fake User Agent
- Other dependencies specified in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/instagram-crawler.git
   cd instagram-crawler
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. The project uses WebDriver Manager to automatically handle the WebDriver for your browser, so no manual installation is required.

## Usage
1. **Run the Script**: You can run the script directly from the command line. Make sure to provide your Instagram username and password:
   ```bash
   python main.py -u your_username -p your_password
   ```

2. **Search Query**: You can customize the search query by using the `-q` option:
   ```bash
   python main.py -u your_username -p your_password -q "your_search_query_here"
   ```

3. **Indexes to Extract**: You can specify which indexes to extract using the `-i` option:
   ```bash
   python main.py -u your_username -p your_password -i 0 1 2 3 4 5 6
   ```

4. Follow the prompts in the console to log in to Instagram if required.

## Configuration
- **Cookie Management**: The crawler saves cookies to maintain login sessions. You can specify your Instagram username and password in the `manual_login_and_save` method in `cookie_manager.py`.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## Acknowledgments
- [Selenium](https://www.selenium.dev/) - For web automation.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - For HTML parsing.
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) - For managing browser drivers.
- [Fake User Agent](https://github.com/helixbass/fake-useragent) - For generating random user agents.

---

# Instagram 爬蟲

## 概述
這個項目是一個 Instagram 爬蟲，允許用戶從 Instagram 地點和貼文中抓取數據。它利用 Selenium 進行網頁自動化，並使用 BeautifulSoup 進行 HTML 解析。該爬蟲可以從指定的 Instagram 地點提取貼文數量、作者和內容等信息。

## 功能
- 根據搜索查詢抓取 Instagram 地點數據。
- 提取貼文信息，包括作者、建立日期和內容。
- 將提取的數據以 JSON 格式保存。
- 支持 cookie 管理以保持登錄狀態。

## 要求
- Python 3.x
- Selenium
- BeautifulSoup4
- WebDriver Manager
- Fake User Agent
- 其他在 `requirements.txt` 中指定的依賴項

## 安裝
1. clone倉庫：
   ```bash
   git clone https://github.com/yourusername/instagram-crawler.git
   cd instagram-crawler
   ```

2. 安裝所需的packages：
   ```bash
   pip install -r requirements.txt
   ```

3. 該項目使用 WebDriver Manager 自動處理瀏覽器的 WebDriver，因此不需要手動安裝。

## 使用
1. **運行腳本**：您可以直接從命令行運行腳本。請確保提供您的 Instagram 用戶名和密碼：
   ```bash
   python main.py -u your_username -p your_password
   ```

2. **搜索查詢**：您可以使用 `-q` 選項自定義搜索查詢：
   ```bash
   python main.py -u your_username -p your_password -q "your_search_query_here"
   ```

3. **提取索引**：您可以使用 `-i` 選項指定要提取的索引：
   ```bash
   python main.py -u your_username -p your_password -i 0 1 2 3 4 5 6
   ```

4. 如果需要，請按照控制台中的提示登錄 Instagram。

## 配置
- **Cookie 管理**：爬蟲保存 cookies 以保持登錄會話。您可以在 `cookie_manager.py` 中的 `manual_login_and_save` 方法中指定您的 Instagram 用戶名和密碼。

## 貢獻
歡迎貢獻！如果您有改進或新功能的建議，請隨時提出問題或提交拉取請求。



## 感謝
- [Selenium](https://www.selenium.dev/) - 用於網頁自動化。
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - 用於 HTML 解析。
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) - 用於管理瀏覽器驅動程序。
- [Fake User Agent](https://github.com/helixbass/fake-useragent) - 用於生成隨機用戶代理。
