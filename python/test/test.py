from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
    
driver = webdriver.Chrome(options=options)
file_path = 'urls.txt'

# 텍스트 파일에서 URL을 읽는 함수
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    # 각 URL의 앞뒤 공백 제거
    urls = [url.strip() for url in urls]
    return urls

# 텍스트 파일에서 URL 읽기

urls = read_urls_from_file(file_path)

# 각 URL에 접근하기
for url in urls:
    driver.get(url)
    time.sleep(5)  # 각 페이지에 5초 대기 (필요에 따라 조정 가능)

# 모든 작업 완료 후 웹드라이버 닫기
driver.quit()
