import os
import multiprocessing
import sys
import pyautogui

def launch():
  # Add path to the growtopia launcher executable here
  os.system("C:/Users/Okko/AppData/Local/Growtopia/Growtopia.exe")


def run():
  process = multiprocessing.Process(target=launch)
  process.start()

def stop():
  if sys.platform == "win32":
    pyautogui.hotkey('alt', 'F4')
  elif sys.platform == "darwin":
    pyautogui.hotkey("command", "q")
