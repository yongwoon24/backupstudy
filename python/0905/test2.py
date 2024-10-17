import requests
import xml.etree.ElementTree as ET
import zipfile
import io
import time
import pandas as pd

# 발급받은 API 인증키를 입력합니다.
api_key = 'a3cb11042acc8e2393eed8a817f76e332b4f8199'

# 1. 모든 기업의 고유번호 가져오기 (기업 고유번호 리스트는 XML 형식으로 제공됨)
url = f'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={api_key}'

# API 요청 보내기
response = requests.get(url)

corp_codes = []  # 기업 고유번호와 이름을 저장할 리스트

# 응답이 성공적인지 확인
if response.status_code == 200:
    # ZIP 파일로 응답이 오기 때문에 메모리에서 압축을 풉니다.
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # ZIP 파일 안에서 corpCode.xml 파일을 엽니다.
        with z.open('CORPCODE.xml') as f:
            # XML 데이터를 파싱합니다.
            tree = ET.parse(f)
            root = tree.getroot()
            
            # 모든 기업의 정보를 순회하면서 고유번호와 기업명을 저장합니다.
            for company in root.findall('list'):
                corp_code = company.find('corp_code').text
                corp_name = company.find('corp_name').text
                corp_codes.append((corp_code, corp_name))

    print(f"총 {len(corp_codes)}개의 기업이 조회되었습니다.")
else:
    print(f"HTTP Request failed with status code {response.status_code}")

# 기업별 주소를 저장할 리스트
company_data = []

# 2. 기업별 주소 조회 및 리스트에 저장
for corp_code, corp_name in corp_codes[:100]:  # 예시로 10개의 기업만 조회
    url = f'https://opendart.fss.or.kr/api/company.json?crtfc_key={api_key}&corp_code={corp_code}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '000':  # 정상 응답인 경우
            adres = data.get('adres', 'N/A')
            company_data.append([corp_name, corp_code, adres])  # 리스트에 기업명, 고유번호, 주소 저장
        else:
            print(f"Error {data['status']}: {data['message']}")
    else:
        print(f"HTTP Request failed with status code {response.status_code}")
    
    # API 요청에 대해 너무 많은 요청을 보내지 않도록 잠시 대기
    time.sleep(0.1)

# 3. pandas DataFrame으로 변환
df = pd.DataFrame(company_data, columns=['기업명', '고유번호', '주소'])

# 4. 엑셀 파일로 저장 (encoding 제거)
df.to_excel('dart_companies.xlsx', index=False)

print("엑셀 파일로 저장되었습니다.")
