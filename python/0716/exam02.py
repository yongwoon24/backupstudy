import pyautogui

fw = pyautogui.getActiveWindow() # 현재 활상화된 창
print(fw.title) #창의 제목 정보
print(fw.size) #창의 크기 정보(width, height)
print(fw.left, fw.top, fw.right, fw.bottom)
pyautogui.click(fw.left+25, fw.top + 20)
print(fw)
#for w in pyautogui.getAllWindows(): #모든 윈도우 가져오기
#    print(w)
    
#타이틀이 포함된 창 활성화, 최대화, 화면 원복, 닫기
#w = pyautogui.getWindowsWithTitle("메모장")[0]  
#if w.isActive == False:
#    w.activate()
#if w.isMaximized == False:
#    w.maximize()
#w.restore() #화면 원복
#w.close()