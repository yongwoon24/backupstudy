import requests
from bs4 import BeautifulSoup
from lxml import etree
import openpyxl as op
wb = op.Workbook()
ws = wb.active
ws.title="한빛도서목록"
titles = "브랜드 도서명 저자 발행일 정가".split()
ws.append(titles)

url = "https://www.hanbit.co.kr/store/books/full_book_list.html?page="
for i in range(1, 10+1):
    
    response = requests.get(url+str(i))
    soup = BeautifulSoup(response.content, 'html.parser')
    book_list_tr = soup.select("table.tbl_type_list tr")
    for j in range(1, len(book_list_tr)):
        scraping_list = []
        book_list_td = book_list_tr[j].select("td")
        for k in range(len(book_list_td)):
            if k == 1 :
                scraping_list.append( book_list_td[k].a.text )
            else : 
                scraping_list.append( book_list_td[k].text )

        ws.append(scraping_list)


wb.save("bookListall.xlsx")
