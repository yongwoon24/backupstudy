import json
import pandas as pd
import oracledb  # Oracle DB와의 연결을 위한 라이브러리
import sys
import uuid
import time
import requests
from openai import OpenAI

# 명령줄 인수로 이미지 경로 받기
if len(sys.argv) != 2:
    print("Usage: python ocr.py <image_file_path>")
    sys.exit(1)

image_file = sys.argv[1]

# API 요청 설정
api_url = 'https://qrzccj1y9c.apigw.ntruss.com/custom/v1/22243/60e2b8a7e366adc85128cffa9fb17254e9c8e9e4a73a7b6eac9c819a718987a3/general'
secret_key = 'ZkhvZFJGUXd2WFRkVWNrWExGc0RXbU9EaVRGYXZuRkc='

# OCR API 요청 데이터 생성
def send_ocr_request():
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
    files = [('file', open(image_file, 'rb'))]
    headers = {'X-OCR-SECRET': secret_key}

    # API 요청 및 응답 처리
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    return response.json()

# 재시도 로직을 포함한 OCR 데이터 처리
def process_ocr_data(json_data):
    string_result = ''
    for field in json_data['images'][0]['fields']:
        linebreak = '\n' if field.get('lineBreak', False) else ' '
        string_result += field.get('inferText', '') + linebreak

    print(string_result)

    # OpenAI API 클라이언트 설정
    client = OpenAI()

    # OpenAI API를 통한 정보 분석 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant to analyze the tracking number, receiver, sender, address, and memo from the invoice and output it in JSON format"},
            {"role": "user", "content": f'please analyze {string_result}. Extract only the tracking number, receiver, sender, address, and memo.'},
        ]
    )
    message = response.choices[0].message.content

    return json.loads(message)

# 재시도 횟수 설정
def retry_if_needed(data, max_retries=3):
    retry_count = 0

    while retry_count < max_retries:
        # 문자열로 받아왔을 때 재시도
        if isinstance(data.get('receiver', ''), str) or isinstance(data.get('sender', ''), str):
            print(f"Retrying... Attempt {retry_count + 1}")
            json_data = send_ocr_request()
            data = process_ocr_data(json_data)
            retry_count += 1
        else:
            # 재시도가 필요 없으면 처리 종료
            break
    
    return data

# 처음으로 OCR 요청 보내기
json_data = send_ocr_request()
data = process_ocr_data(json_data)

# 문자열인 경우 재시도 로직 실행
data = retry_if_needed(data)

# 재시도 후에도 실패할 경우 예외 처리
if isinstance(data.get('receiver', ''), str) or isinstance(data.get('sender', ''), str):
    print("Failed to extract structured data after maximum retries.")
else:
    # 데이터 저장 로직 실행
    tracking_number = data.get('tracking_number', 'N/A')
    
    # 전화번호 필드를 처리하는 함수
    def extract_phone_number(entity):
        if isinstance(entity, dict):
            phones = entity.get('phone', []) or entity.get('phone_numbers', []) or [entity.get('phone_number', 'N/A')] or entity.get('contact', 'N/A') or [entity.get('contact_number', 'N/A')]
            if isinstance(phones, list):
                phones = ''.join([str(p) for p in phones])  # 리스트를 문자열로 변환
            if isinstance(phones, str):
                phones = phones.replace(',', '').replace(' ', '')  # 공백과 쉼표 제거
            return phones
        elif isinstance(entity, str):
            return entity.replace(',', '').replace(' ', '')  # 문자열로 반환된 경우 처리
        return None

    # Receiver 처리
    receiver = data.get('receiver', {})
    if isinstance(receiver, dict):
        receiver_name = receiver.get('name', None)
        receiver_phone_numbers = extract_phone_number(receiver)
        receiver_address = receiver.get('address', None)
    elif isinstance(receiver, str):
        receiver_name = receiver
        receiver_phone_numbers = None
        receiver_address = None

    # Sender 처리
    sender = data.get('sender', {})
    if isinstance(sender, dict):
        sender_name = sender.get('name', None)
        sender_phone_number = extract_phone_number(sender)
        sender_address = sender.get('address', None)
    elif isinstance(sender, str):
        sender_name = sender
        sender_phone_number = None
        sender_address = None

    # Memo 처리
    memo = data.get('memo', None)
    memo_str = '\n'.join(memo) if isinstance(memo, list) else memo

    # 데이터프레임 생성
    df = pd.DataFrame([{
        '운송번호': tracking_number,
        '받는분이름': receiver_name,
        '받는분휴대폰번호': receiver_phone_numbers,
        '받는분주소': receiver_address,
        '보내는분이름': sender_name,
        '보내는분휴대폰번호': sender_phone_number,
        '보내는분주소': sender_address,
        '메모': memo_str  # 메모를 문자열로 저장
    }])

    print("Dataframe created:", df)

    # Oracle 클라이언트 초기화
    oracledb.init_oracle_client(lib_dir="C:/Users/3calss_15/Downloads/instantclient_11_2")

    # Oracle 데이터베이스에 연결 및 예외 처리
    dsn = oracledb.makedsn('localhost', 1521, service_name='xe')
    try:
        connection = oracledb.connect(user='mainproject', password='mainproject', dsn=dsn)
        print("Oracle DB connection successful.")
    except oracledb.DatabaseError as e:
        print(f"Error connecting to Oracle Database: {e}")
        sys.exit(1)

    # 데이터베이스에 데이터 저장 함수
    def save_to_db(df):
        cursor = connection.cursor()  # 커서 생성

        # 데이터프레임의 각 행을 반복하여 DB에 삽입
        for index, row in df.iterrows():
            receiver_name = row['받는분이름'] if row['받는분이름'] is not None else None
            receiver_phone_numbers = row['받는분휴대폰번호'] if row['받는분휴대폰번호'] is not None else None
            receiver_address = row['받는분주소'] if row['받는분주소'] is not None else None

            sender_name = row['보내는분이름'] if row['보내는분이름'] is not None else None
            sender_phone_number = row['보내는분휴대폰번호'] if row['보내는분휴대폰번호'] is not None else None
            sender_phone_number = sender_phone_number.replace(',', '').replace(' ', '') if sender_phone_number else None
            sender_address = row['보내는분주소'] if row['보내는분주소'] is not None else None

            memo = row['메모'] if row['메모'] is not None else None

            # 데이터를 Oracle DB에 삽입
            cursor.execute('''
                INSERT INTO DELIVERY 
                (DELIVERY_NUMBER, RECEIVER, RECEIVER_PHONE, RECEIVER_ADDRESS, SENDER, SENDER_PHONE, SENDER_ADDRESS, MEMO)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            ''', (row['운송번호'], receiver_name, receiver_phone_numbers, receiver_address, 
                  sender_name, sender_phone_number, sender_address, memo))

            print(f"Inserted row: {row}")

        connection.commit()  # 변경 사항을 DB에 저장
        cursor.close()  # 커서 닫기

    # DB에 저장 호출
    save_to_db(df)

    # 연결 종료
    connection.close()  # DB 연결 종료
