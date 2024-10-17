import pyautogui
import sys

size = (1,1) 
print("size() => ", pyautogui.size())
if(pyautogui.size()[0] != 1920 or pyautogui.size()[1] != 1200 ):
    sys.exit()

print(type(size))
print("exit check")
