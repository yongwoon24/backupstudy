import os
import pytesseract
from PIL import Image
import cv2
from pywinauto import Application

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

# 이미지에서 텍스트 추출
def extract_text_from_image(image_path):
    # 이미지 전처리
    preprocessed_image = preprocess_image(image_path)
    
    # Tesseract 설정
    custom_config = r'--oem 3 --psm 6'
    
    # 텍스트 추출
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config, lang='kor')
    return text

# 디렉토리 내 이미지 파일 목록 가져오기
def get_image_files(directory):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(valid_extensions)]

def save_text_to_word(text):
    # MS Word 실행 경로 설정
    word_path = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"  # 실제 경로로 수정하세요
    
    # MS Word 실행
    app = Application().start(word_path)
    
    # Word 창 선택
    dlg = app.top_window()
    
    # "파일" 메뉴 클릭 후 "새 문서" 선택
    dlg.menu_select("파일->새로 만들기")
    
    # 텍스트 입력
    dlg.type_keys(text, with_spaces=True)
    
    # 문서 저장
    dlg.menu_select("파일->다른 이름으로 저장")
    dlg.type_keys("extracted_text.docx", with_spaces=True)  # 파일명 입력
    dlg.type_keys("{ENTER}", with_spaces=True)  # 저장 확인

# 메인 함수
def main():
    # 이미지 파일들이 있는 디렉토리 경로 설정
    directory = 'C:\\RPAWork\\workspace\\python\\testimgs'  # 이미지 파일이 있는 디렉토리 경로 설정
    
    # 디렉토리 내 이미지 파일 목록 가져오기
    image_files = get_image_files(directory)
    
    # 각 이미지 파일에서 텍스트 추출 및 Word에 저장
    for image_path in image_files:
        text = extract_text_from_image(image_path)
        save_text_to_word(text)
        print(f"Processed: {image_path}")

if __name__ == "__main__":
    main()
