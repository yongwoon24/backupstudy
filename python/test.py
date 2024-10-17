marks = [100, 65, 100,100, 55] #정보처리 기사 시험의 각 과목별 점수
# 합격 불합격을 판단하는 프로그램을 작성하시오...
sum = 0
marks.sort() #오름차순으로 리스트이 내용을 정렬
panjumg = '불합격'
for jum in marks:
    if jum < 40 : # 과락 검증
#        sum = 299 
        break
    sum += jum
if sum / len(marks) >=60 :
    panjumg = "합격"
print( panjumg)