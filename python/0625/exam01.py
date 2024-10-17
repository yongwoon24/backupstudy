import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_experimental_option("detach", True)

browser = webdriver.Chrome()
url = "https://www.naver.com"
url2 = "https://www.daum.net"

browser.get(url)
time.sleep(2)

browser.get(url2)
time.sleep(3)

browser.back()
time.sleep(1)
browser.refresh()
time.sleep(3)
browser.forward()
time.sleep(5)



# query = browser.find_element(By.CSS_SELECTOR, "#account > div > p")
# print(query.text)