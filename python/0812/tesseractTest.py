import pytesseract
from PIL import Image
import openpyxl
from openpyxl import Workbook
import cv2
import numpy as np
import os

# Tesseract OCR 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 전처리 함수
def preprocess_image(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # 이미지 크기 조정
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 노이즈 제거
    image = cv2.medianBlur(image, 3)
    
    # 이미지 이진화
    _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return image

# Bounding box를 이용한 텍스트 영역 시각화 함수
def visualize_text_boxes(image_path):
    # 이미지 전처리
    image = preprocess_image(image_path)
    
    # Tesseract로 bounding box 정보 얻기
    boxes = pytesseract.image_to_boxes(image, lang='kor')
    
    # 컬러 이미지로 변환
    color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    h, w = color_image.shape[:2]
    
    # bounding box 그리기
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(color_image, (x, h-y), (x2, h-y2), (0, 255, 0), 2)
    
    # bounding box가 그려진 이미지 저장
    cv2.imwrite('text_boxes.png', color_image)
    
    # bounding box가 그려진 이미지 출력
    cv2.imshow('Text Boxes', color_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 이미지에서 텍스트 추출
def extract_text_from_image(image_path):
    # 이미지 전처리
    preprocessed_image = preprocess_image(image_path)
    
    # Tesseract 설정
    custom_config = r'--oem 3 --psm 6'
    
    # 텍스트 추출
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config, lang='kor')
    return text

# 텍스트를 엑셀 파일에 저장
def save_text_to_excel(text, excel_path):
    wb = Workbook()
    ws = wb.active
    lines = text.split('\n')
    
    for i, line in enumerate(lines, start=1):
        ws.cell(row=i, column=1, value=line)
    
    wb.save(excel_path)

# 메인 함수
def main():
    # 현재 작업 디렉토리에서 상위 폴더의 이미지 파일 경로 설정
    image_path = 'testimg03.jpg'  # 상위 폴더의 파일 경로
    excel_path = 'receipt_data.xlsx'  # 저장할 엑셀 파일 경로

    if not os.path.isfile(image_path):
        print(f"Image file not found: {image_path}")
        return

    # 텍스트 영역 시각화
    visualize_text_boxes(image_path)
    
    # 이미지에서 텍스트 추출
    text = extract_text_from_image(image_path)
    print("Extracted Text:", text)
    
    # 텍스트를 엑셀에 저장  
    save_text_to_excel(text, excel_path)
    print(f"Text saved to {excel_path}")

if __name__ == "__main__":
    main()
