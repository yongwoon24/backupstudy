count = 0
options = ['이름', '주소', '전화번호', '나이', '키']
f = open('sample2.csv', 'a', newline='', encoding='utf-8')
print('자료를 더 이상 입력하지 않으려면 false를 입력하세요')
while True:
    data = input(f'{options[count]}를 입력하세요 : ')
    if data.strip() == 'false':
        break
    
    f.write(data)
    count += 1
    
    if count % 5 == 0:
        f.write("\n")
    else:
        f.write(",")
    
    if count == len(options):
        count = 0

f.close()
