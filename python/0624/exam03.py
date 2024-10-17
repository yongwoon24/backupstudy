from bs4 import BeautifulSoup
html = '''
<html>
    <body>
        <h1>스크래핑 테스트</h1>
        <p id="first">웹 페이지의 첫번째 문단입니다</p>
        <p class="second">두번째 문단입니다.</p>
        <a data_anc="yangdoll" href="hreftest">href</a>
        
    </body>
</html>
'''
soup = BeautifulSoup(html, 'html.parser')
print("result ==> ", soup)
print(soup.html.p)

p1 = soup.html.p
p2 = p1.next_sibling.next_sibling
print(p2)

idfind = soup.find(id='first')
classfind = soup.find(class_='second')
data_ancFind = soup.find(data_anc='yangdoll')
print(idfind, classfind, data_ancFind)