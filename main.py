import time
import json
import pyautogui
from launcher import run
from launcher import stop

PUNCH_KS = "e"

JUMP_KS = "w"
LEFT_KS = "a"
RIGHT_KS = "d"

DOOR_TO_FIRST_S = 2.1

CYCLE_COOLDOWN = 10.5

MOVE_CYCLES_ROW = 2

with open('./config.json') as f:
  config = json.load(f)
  f.close()
MIDDLE = config["middle"]

SCREEN_WIDTH = config["screen"]["width"]
SCREEN_HEIGTH = config["screen"]["height"]

TOP = config["screen"]["top"]
LEFT = config["screen"]["left"]


class Harvester():

  def __init__(self, conf) -> None:
    self.rows = conf["filled_rows"]

  def full_harvest(self):
    for row in range(1, self.rows+1):
      print("Harvesting row", row)
      self.harvest_row(row)


  def harvest_row(self, row):
    go_to_row(row)
    time.sleep(1.5)
    # for i in range(MOVE_CYCLES_ROW):
    #   pyautogui.keyDown(RIGHT_KS)
    #   pyautogui.keyDown(PUNCH_KS)
    #   time.sleep(CYCLE_COOLDOWN)
    #   pyautogui.keyUp(RIGHT_KS)
    #   pyautogui.keyUp(PUNCH_KS)

    respawn()


class Controller():

  def __init__(self, conf) -> None:
    self.conf = conf

  def initialize():
    run()
    input("Press Enter to start...")
    set_screen()
    start()

  def cycle(self, hours):

    self.initialize()
    farmer = Harvester(self.conf)
    for i in range(2):
      farmer.full_harvest()
      stop() # Close the game
      time.sleep(30) 
      # time.sleep(60*60*hours)

      run() # start the game
      time.sleep(3)
      set_screen()
      start(self.conf) # Initialize  in-game


def set_screen():
  global MIDDLE
  global SCREEN_HEIGTH
  global SCREEN_WIDTH
  global TOP
  global LEFT
  this = pyautogui.getWindowsWithTitle("Growtopia")
  print(this[0])
  x_middle = this[0].left + this[0].width/2
  y_middle = this[0].top + this[0].height/2
  with open('./config.json', 'r') as f:
    config = json.load(f)
    config["middle"] = {"x": x_middle, "y": y_middle}
    config["screen"] = {"width": this[0].width, "height": this[0].height, "top": this[0].top, "left": this[0].left}
  with open('./config.json', 'w') as f:
    json.dump(config, f, indent=2)
  MIDDLE = config["middle"]
  SCREEN_WIDTH = this[0].width
  SCREEN_HEIGTH = this[0].height
  TOP = this[0].top
  LEFT = this[0].left
  


def start(config):
  print(f"""
  Screen h: {SCREEN_HEIGTH}
  Screen w: {SCREEN_WIDTH}
  Top: {TOP}
  Left: {LEFT}
  """)
  # play button
  pyautogui.click(
    x=MIDDLE["x"],
    y=MIDDLE["y"] + SCREEN_HEIGTH * 0.1,
    duration=0.5
  )
  time.sleep(0.5)

  # Enter
  enter_world()

  time.sleep(10)
  # banner
  pyautogui.click(
    x=MIDDLE["x"],
    y=TOP + SCREEN_HEIGTH*0.4,
    duration=0.5
  )

  time.sleep(3)
  # survey popup
  close_popup()
  time.sleep(3)

  # enter world
  enter_world()

  time.sleep(10)
  fix_zoom_lvl()

  print("Harvester ready")


def go_to_row(row: int):
  pyautogui.keyDown(RIGHT_KS)
  time.sleep(DOOR_TO_FIRST_S)
  pyautogui.keyUp(RIGHT_KS)
  if 1 < row <= 21:
    for _ in range(1, row):
      pyautogui.keyDown(JUMP_KS)
      time.sleep(1.5)
      pyautogui.keyUp(JUMP_KS)
  elif row == 1:
    pass
  else:
    print("Something went wrong [TRIED TO GO TO A ROW THAT DOES NOT EXIST]")

def respawn():
  # top right menu
  pyautogui.click(
    x=LEFT + SCREEN_WIDTH*0.95,
    y=TOP + SCREEN_HEIGTH * 0.1,
    duration=0.75
  )
  time.sleep(0.5)
  pyautogui.click(
    x=MIDDLE["x"],
    y=TOP + SCREEN_HEIGTH * 0.30,
    duration=0.75
  )
  time.sleep(5)

def enter_world():
  # enter world button
  pyautogui.click(
    x=LEFT + SCREEN_WIDTH * 0.75,
    y=TOP + SCREEN_HEIGTH * 0.9,
    duration=0.75
  )

def close_popup():
  pyautogui.click(
    x=LEFT + SCREEN_WIDTH * 0.18,
    y=TOP + SCREEN_HEIGTH * 0.72,
    duration=0.75
  )

def fix_zoom_lvl():
  for _ in range(25):
    pyautogui.scroll(10, MIDDLE["x"], MIDDLE["y"])


def main():

  with open('./config.json') as f:
    config = json.load(f)

  # initialize controller
  controller = Controller(config)
  controller.cycle(12)


if __name__ == "__main__":
  main()