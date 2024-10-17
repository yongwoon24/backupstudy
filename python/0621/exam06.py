import csv

def main():
    data = []
    print("데이터를 입력하세요. 입력이 끝나면 false를 입력하세요.")
    while True:
        line = input("데이터 입력: ")
        if line.strip() == 'false':
            break
        data.append(line)
    
    with open('sample2.csv', 'w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        for i in range(0, len(data), 5):
            wr.writerow(data[i:i+5])
    
    print("CSV 파일이 저장되었습니다.")
    print(data)

if __name__ == "__main__":
    main()
