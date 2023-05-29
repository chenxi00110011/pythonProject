import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 3

# while True:
#     pyautogui.moveRel(100,0)
#     print('wait')


def getLocation():
    print(pyautogui.position())
    return pyautogui.position()

def click(fileName):
    url = f'C:\\Users\\Administrator\\Desktop\\picture\\{fileName}.png'
    time.sleep(0.5)    # 等待 0.5 秒
    left, top, width, height = pyautogui.locateOnScreen(url)   # 寻找图片；
    center = pyautogui.center((left, top, width, height))    # 寻找图片的中心
    pyautogui.click(center)

time.sleep(5)
# 图像识别（一个）
# btm = pyautogui.locateOnScreen(url)
# print(btm)  # Box(left=1280, top=344, width=22, height=22)
# click('刷新列表')
# if click('已')
# click('全选')
# click('固件升级')
# click('确定1')
# pyautogui.click(252,141)
# time.sleep(120)
# click('确定2')