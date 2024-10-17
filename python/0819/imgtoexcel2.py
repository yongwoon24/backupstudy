import os
import time
import pytesseract
from PIL import Image
import cv2
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# Tesseract OCR 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 전처리 함수
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    image = cv2.medianBlur(image, 3)
    _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return image

# 이미지에서 텍스트 추출
def extract_text_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    custom_config = r'--oem 3 --psm 6 -l eng+kor'
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    print(f"Extracted Text from {image_path}: \n{text}\n")
    return text

# 디렉토리 내 이미지 파일 목록 가져오기
def get_image_files(directory):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(valid_extensions)]

# 텍스트를 Excel에 저장하는 함수
def save_text_to_excel(texts, file_path):
    excel_path = r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
    app = Application().start(excel_path)
    
    time.sleep(5)
    
    # Desktop 객체를 사용하여 Excel 창 식별
    excel_window = app.window(title_re=".*Excel.*")

    if not excel_window:
        raise Exception("Excel 창을 찾을 수 없습니다.")
    
    # 새 통합 문서 생성 (Ctrl + N)
    excel_window.type_keys('^n')
    time.sleep(2)
    
    # 각 텍스트를 셀에 입력
    for index, text in enumerate(texts):
        # 셀에 텍스트 입력
        excel_window.type_keys(f'{text}{"{ENTER}"}', with_spaces=True)
        if index < len(texts) - 1:
            send_keys('{DOWN}')
        time.sleep(1)
    
    # 파일 저장 (Ctrl + S)
    excel_window.type_keys('^s')
    time.sleep(2)
    
    # 파일 경로 입력 후 저장
    save_as_window = app.window(title_re=".*Save As.*")
    if save_as_window.exists():
        save_as_window.type_keys(file_path + "{ENTER}", with_spaces=True)

# 메인 함수
def main():
    directory = 'C:\\RPAWork\\workspace\\python\\testimgs'
    image_files = get_image_files(directory)
    
    texts = []
    for image_path in image_files:
        text = extract_text_from_image(image_path)
        texts.append(text)
        print(f"Processed: {image_path}")

    # 엑셀 파일에 텍스트 저장
    save_text_to_excel(texts, 'C:\\RPAWork\\workspace\\python\\extracted_text.xlsx')

if __name__ == "__main__":
    main()
