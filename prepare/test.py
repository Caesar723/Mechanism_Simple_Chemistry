import pyautogui
import time


time.sleep(1)
for i in range(1000):
    pyautogui.keyDown("command")
    pyautogui.keyDown("v")
    pyautogui.keyUp("v")
    pyautogui.keyUp("command")

    pyautogui.keyDown("enter")
    pyautogui.keyUp("enter")

print(1)

