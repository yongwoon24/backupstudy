import oracledb  # cx_Oracle 대신 oracledb 사용
import json
import requests
import uuid
import time
import pandas as pd
import sys
import os

# 예외 처리 추가 (파일 경로 확인)
if not os.path.exists(sys.argv[1]):
    print(f"Error: File {sys.argv[1]} not found.")
    sys.exit(1)

# 이미지를 첨부한 파일 경로를 명령줄 인수로 받음
image_file = sys.argv[1]

# API 요청 설정
api_url = 'https://qrzccj1y9c.apigw.ntruss.com/custom/v1/22243/60e2b8a7e366adc85128cffa9fb17254e9c8e9e4a73a7b6eac9c819a718987a3/general'
secret_key = 'ZkhvZFJGUXd2WFRkVWNrWExGc0RXbU9EaVRGYXZuRkc='

# OCR API 요청 데이터 생성
request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'invoice'  
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
    ('file', open(image_file, 'rb'))
]
headers = {
    'X-OCR-SECRET': secret_key
}

# OCR API 호출 및 예외 처리 추가
try:
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    response.raise_for_status()  # 응답 상태 코드 확인
    json_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error during OCR API request: {e}")
    sys.exit(1)

# OCR 결과 문자열 생성
string_result = ''
for i in json_data['images'][0]['fields']:
    if i['lineBreak'] == True:
        linebreak = '\n'
    else:
        linebreak = ' '
    string_result = string_result + i['inferText'] + linebreak

print(string_result)

# JSON 파일로 저장
json_file_path = 'C:\\RPAWork\\workspace\\mainproject\\mainProject\\json'

with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)

# 분석된 데이터 처리
tracking_number = "추출된 운송번호"  # 운송번호 추출하는 로직 적용
receiver_name = "추출된 받는 사람 이름"
receiver_phone = "추출된 받는 사람 번호"
receiver_address = "추출된 받는 사람 주소"
sender_name = "추출된 보내는 사람 이름"
sender_phone = "추출된 보내는 사람 번호"
sender_address = "추출된 보내는 사람 주소"
memo = "추출된 메모"

# 데이터프레임 생성
df = pd.DataFrame([{
    '운송번호': tracking_number,
    '받는분이름': receiver_name,
    '받는분휴대폰번호': receiver_phone,
    '받는분주소': receiver_address,
    '보내는분이름': sender_name,
    '보내는분휴대폰번호': sender_phone,
    '보내는분주소': sender_address,
    '메모': memo
}])

# Oracle 데이터베이스에 연결 (oracledb 사용) 및 예외 처리 추가
dsn = oracledb.makedsn('localhost', 1521, service_name='xe')  # DSN 생성
try:
    connection = oracledb.connect(user='mainproject', password='mainproject', dsn=dsn)
except oracledb.DatabaseError as e:
    print(f"Error connecting to Oracle Database: {e}")
    sys.exit(1)

# 데이터베이스에 데이터 저장 함수
def save_to_db(df):
    cursor = connection.cursor()  # 커서 생성
    
    # 데이터프레임의 각 행을 반복하여 DB에 삽입
    for index, row in df.iterrows():
        try:
            print(f"Inserting row: {row}")  # 추가된 로그: 삽입할 데이터를 출력
            cursor.execute('''
                INSERT INTO DELIVERY 
                (DELIVERY_NUMBER, RECEIVER, RECEIVER_PHONE, RECEIVER_ADDRESS, SENDER, SENDER_PHONE, SENDER_ADDRESS, MEMO)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            ''', (row['운송번호'], row['받는분이름'], row['받는분휴대폰번호'], row['받는분주소'], 
                  row['보내는분이름'], row['보내는분휴대폰번호'], row['보내는분주소'], row['메모']))
        except oracledb.DatabaseError as e:
            print(f"Error inserting data into Oracle DB: {e}")  # 추가된 로그: DB 오류를 출력
            connection.rollback()
        else:
            connection.commit()  # 변경 사항을 DB에 저장
    cursor.close()  # 커서 닫기


# DB에 저장 호출
save_to_db(df)

# 연결 종료
connection.close()  # DB 연결 종료
