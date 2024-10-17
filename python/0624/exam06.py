import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook

publishers = []
titles = []
writers = []
dates = []
prices = []
links = []
for page in range(1, 11):
    url = f"https://www.hanbit.co.kr/store/books/full_book_list.html?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    book_items = soup.select("tbody > tr")

    for item in book_items:
        publisher = item.select_one("td:nth-of-type(1)").text.strip()
        title = item.select_one("td.left a").text.strip()
        writer = item.select_one("td.left").find_next_sibling().text.strip()
        date = item.select_one("td:nth-of-type(4)").text.strip()
        price = item.select_one("td.right").text[1:].replace(",", "").replace("원", "")
        link = "https://www.hanbit.co.kr" + item.select_one("td.left a")['href']

        # print(f"출판사: {publisher}")
        # print(f"제목: {title}")
        # print(f"저자: {writer}")
        # print(f"출판일: {date}")
        # print(f"가격: {price}")
        # print(f"링크: {link}")
        # print("=" * 50)

        publishers.append(publisher)
        titles.append(title)
        writers.append(writer)
        dates.append(date)
        prices.append(price)
        links.append(link)


new_data = {
    '일련번호': range(1, len(titles) + 1),
    '출판사' : publishers,
    '제목': titles,
    '저자': writers,
    '출판일' : dates,
    '가격': prices,
    '링크': links
}
new_df = pd.DataFrame(new_data)

existing_excel_filename = '한빛도서리스트2.xlsx'
try:
    existing_df = pd.read_excel(existing_excel_filename, engine='openpyxl')
except FileNotFoundError:
    existing_df = pd.DataFrame(columns=['일련번호', '출판사', '제목', '저자', '출판일', '가격', '링크'])

if set(new_df.columns) == set(existing_df.columns):
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)

    with pd.ExcelWriter(existing_excel_filename, engine='openpyxl', mode='w') as ew:
        combined_df.to_excel(ew, index=False)

    # 엑셀 파일 열기
    wb = load_workbook(existing_excel_filename)
    sheet = wb.active

    # 컬럼 폭 조절 (예시로 제목과 저자 폭을 조절)
    sheet.column_dimensions['A'].width = 5
    sheet.column_dimensions['B'].width = 10  
    sheet.column_dimensions['C'].width = 80
    sheet.column_dimensions['D'].width = 40
    sheet.column_dimensions['E'].width = 20
    sheet.column_dimensions['G'].width = 90    

    # 엑셀 파일 저장
    wb.save(existing_excel_filename)
    print(f"데이터가 추가되었습니다 '{existing_excel_filename}'.")
else:
    print("데이터가 추가되지 않았습니다.")

