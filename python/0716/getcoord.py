import pyautogui
import time

print("마우스를 움직여 좌표를 확인하세요. 종료하려면 Ctrl+C를 누르세요.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"현재 좌표: ({x}, {y})", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")