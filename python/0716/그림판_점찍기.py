import pyautogui
import time
import subprocess

subprocess.Popen('mspaint')

time.sleep(2)
pyautogui.getActiveWindow().maximize()
def click_at(x, y):
    pyautogui.moveTo(x, y, duration=1.0) 
    time.sleep(0.5)
    pyautogui.click()

coordinates = [(100, 200), (200, 300), (300, 400)]


click_at(867, 64)
click_at(673, 106)
click_at(713, 268)

for coord in coordinates:
    click_at(*coord)
    time.sleep(0.5)  
click_at(991, 81)
click_at(485, 66)
pyautogui.moveTo(400, 400, duration=1)
pyautogui.drag(400,400,2)

click_at(332, 73)
click_at(554, 595)
click_at(184, 99)
click_at(160, 278)

pyautogui.typewrite('Hello world!', interval=0.1)
click_at(554, 795)

