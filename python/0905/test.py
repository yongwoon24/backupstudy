import requests
import json

# 발급받은 API 인증키를 입력합니다.
api_key = 'a3cb11042acc8e2393eed8a817f76e332b4f8199'

# 공시 대상 회사의 고유번호를 입력합니다. (예: 삼성전자의 고유번호)
corp_code = '00126380'

# DART Open API URL 설정
url = f'https://opendart.fss.or.kr/api/company.json?crtfc_key={api_key}&corp_code={corp_code}'

# API 요청 보내기
response = requests.get(url)

# 응답이 성공적인지 확인 (HTTP 상태 코드 200은 성공을 의미)
if response.status_code == 200:
    # JSON 데이터를 파싱
    data = response.json()
    
    # 결과 출력
    if data['status'] == '000':  # 정상 응답인지 확인
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print(f"Error {data['status']}: {data['message']}")
else:
    print(f"HTTP Request failed with status code {response.status_code}")
