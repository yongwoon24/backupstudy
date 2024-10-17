f = open("test.txt", "r", encoding='utf-8')
#print(f.read())
indata = f.read()
in_lines = indata.split('\n')
words = []
for line in in_lines:
    for word in line.split():
        words.append(word)
target_word = "사랑"
count = indata.count(target_word)
print(count)
f.close
print(words)