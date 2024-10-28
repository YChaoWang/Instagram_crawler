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

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- [Selenium](https://www.selenium.dev/) - For web automation.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - For HTML parsing.
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) - For managing browser drivers.
- [Fake User Agent](https://github.com/helixbass/fake-useragent) - For generating random user agents.
