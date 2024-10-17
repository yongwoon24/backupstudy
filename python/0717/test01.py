import pyautogui
import subprocess

subprocess.Popen('mspaint')

pyautogui.sleep(2)
pyautogui.getActiveWindow().maximize()
pyautogui.sleep(5)
result = pyautogui.locateOnScreen("test.png")
pyautogui.click(result)