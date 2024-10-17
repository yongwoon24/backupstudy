f = open("test.txt", "r", encoding='utf-8')
indata = f.read()

target_word = "사랑"
count = indata.count(target_word)

print(f"'{target_word}' 단어의 개수는 {count}개 입니다.")
f.close()