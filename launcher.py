import os
import multiprocessing

def launch():
  # print("\nLaunching Growtopia\n")
  os.system("C:/Users/Okko/AppData/Local/Growtopia/Growtopia.exe")


def run():
  process = multiprocessing.Process(target=launch)
  process.start()

def stop():
  os.system("TASKKILL /F /IM Growtopia.exe")