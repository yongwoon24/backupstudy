import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Chrome WebDriver 옵션 설정
options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://naver.com")
elem = driver.find_element(By.CSS_SELECTOR, "#query")
elem.send_keys("채상병특검")
elem.send_keys(Keys.ENTER)
articles = []
article_elements = driver.find_elements(By.CSS_SELECTOR, 'li.bx')

with open('newsSearch.csv', 'w', encoding='utf-8-sig', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['제목', '내용'])  
    
    for article in article_elements:
        try:
            news_title = article.find_element(By.CSS_SELECTOR, 'a.news_tit').text.strip()
            news_content = article.find_element(By.CSS_SELECTOR, 'div.news_dsc div.dsc_wrap').text.strip()
            
            wr.writerow([news_title, news_content])
            
            articles.append({'제목': news_title, '내용': news_content})
        except Exception as e:
            print(f"기사 정보를 가져오는 중 오류 발생: {str(e)}")

driver.quit()

print("수집한 기사 개수:", len(articles))
print("기사 제목 및 내용:")
for idx, article in enumerate(articles, start=1):
    print(f"{idx}. 제목: {article['제목']}")
    print(f"   내용: {article['내용']}")
    print("-" * 50)
