import requests
from bs4 import BeautifulSoup
from lxml import etree

response = requests.get("https://hanbit.co.kr/media/books/category_list.html?cate_cd=001001")
soup = BeautifulSoup(response.content, 'html.parser')
select_element = soup.select_one("div.sub_book_list_area>ul>li.sub_book_list")
print(select_element)

