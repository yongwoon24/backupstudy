import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook

url = "https://hanbit.co.kr/media/books/category_list.html?cate_cd=001001"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

book_items = soup.select("div.sub_book_list_area > ul > li.sub_book_list")

titles = []
writers = []
prices = []
links = []

for item in book_items:
    book_title = item.select_one("p.book_tit a").text
    book_writer = item.select_one("p.book_writer").text
    book_price = item.select_one("span.price").text[1:].replace(",", "")
    book_link = "https://hanbit.co.kr/media/books/" + item.select_one("p.book_tit a")['href'][2:]

    titles.append(book_title)
    writers.append(book_writer)
    prices.append(book_price)
    links.append(book_link)

new_data = {
    '일련번호': range(1, len(book_items) + 1),
    '제목': titles,
    '저자': writers,
    '가격': prices,
    '링크': links
}
new_df = pd.DataFrame(new_data)

existing_excel_filename = '한빛도서리스트.xlsx'
try:
    existing_df = pd.read_excel(existing_excel_filename, engine='openpyxl')
except FileNotFoundError:
    existing_df = pd.DataFrame(columns=['일련번호', '제목', '저자', '가격', '링크'])

if set(new_df.columns) == set(existing_df.columns):
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)

    with pd.ExcelWriter(existing_excel_filename, engine='openpyxl', mode='w') as writer:
        combined_df.to_excel(writer, index=False)

    # 엑셀 파일 열기
    wb = load_workbook(existing_excel_filename)
    sheet = wb.active

    # 컬럼 폭 조절 (예시로 제목과 저자 폭을 조절)
    sheet.column_dimensions['B'].width = 50  
    sheet.column_dimensions['C'].width = 40  
    sheet.column_dimensions['E'].width = 80  

    # 엑셀 파일 저장
    wb.save(existing_excel_filename)
    print(f"데이터가 추가되었습니다 '{existing_excel_filename}'.")
else:
    print("데이터가 추가되지 않았습니다.")
