import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://naver.com")
shortcut_link = driver.find_element(By.CSS_SELECTOR, '#shortcutArea > ul > li:nth-child(6) > a')
shortcut_link.click()

new_tab = driver.window_handles[-1]
driver.switch_to.window(new_tab)

menu_link = driver.find_element(By.CSS_SELECTOR, '#content > div.article > div.section > div.section_sise_top > div.group_type.is_active > a')
menu_link.click()

rows = driver.find_elements(By.CSS_SELECTOR, 'table.type_2 tbody tr')

data = []

for row in rows:
    cells = row.find_elements(By.CSS_SELECTOR, 'td')
    if len(cells) >= 11:
        item = cells[1].text.strip()
        current_price = cells[2].text.strip()
        yday = cells[3].text.strip()
        change_rate = cells[4].text.strip()
        trade_amount = cells[5].text.strip()
        trade_price = cells[6].text.strip()
        buy_price = cells[7].text.strip()
        sell_price = cells[8].text.strip()
        total_price = cells[9].text.strip()
        per = cells[10].text.strip()
        roe = cells[11].text.strip()
        data.append([item, current_price, yday, change_rate, trade_amount, trade_price, buy_price, sell_price, total_price, per, roe])

driver.quit()

# pandas DataFrame 생성
df = pd.DataFrame(data, columns=['종목명', '현재가', '전일비', '등락률', '거래량', '거래대금', '매수호가', '매도호가', '시가총액', 'PER', 'ROE'])

# 엑셀 파일로 저장
excel_filename = 'stock_data2.xlsx'
df.to_excel(excel_filename, index=False)

print(f"엑셀 파일 '{excel_filename}'이 저장되었습니다.")
