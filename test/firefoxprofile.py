from selenium import webdriver

myprofile = webdriver.FirefoxProfile()
gecko_driver_path = "/Users/wangyichao/gekodriver/geckodriver"
driver = webdriver.Firefox(
    firefox_profile=myprofile,
    executable_path=gecko_driver_path,
)
driver.get("https://www.instagram.com")
print("Page Title is : %s" % driver.title)
input("Press Enter to close...")
driver.quit()
