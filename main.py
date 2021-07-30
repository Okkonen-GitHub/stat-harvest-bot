from logger import Logger
import time
import json
import pyautogui
from launcher import run
from launcher import stop
logger = Logger()

PUNCH_KS = "e"

JUMP_KS = "w"
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
      self.harvest_row(row)


  def harvest_row(self, row):
    go_to_row(row)
    time.sleep(1.25)
    for _ in range(MOVE_CYCLES_ROW):
      pyautogui.keyDown(RIGHT_KS)
      pyautogui.keyDown(PUNCH_KS)
      time.sleep(CYCLE_COOLDOWN)
      pyautogui.keyUp(RIGHT_KS)
      pyautogui.keyUp(PUNCH_KS)

    respawn()
    logger.add_log(f"harvested {row}")


class Controller():

  def __init__(self, conf) -> None:
    self.conf = conf

  def cycle(self, hours):

    farmer = Harvester(self.conf)

    for i in range(2):
      run() # start the game
      logger.add_log("Launch the game")
      time.sleep(4)
      set_screen()
      start() # Initialize  in-game

      farmer.full_harvest()
      logger.add_log("Harvested")

      stop() # Close the game
      if i < 1:
        logger.add_log(f"Waiting {hours} hours")
        time.sleep(60*60*hours - 60*5) # minus 5 minutes
      if i < 0:
        logger.add_log("Second harvest done")


def set_screen():
  global MIDDLE
  global SCREEN_HEIGTH
  global SCREEN_WIDTH
  global TOP
  global LEFT
  this = pyautogui.getWindowsWithTitle("Growtopia")
  if len(this) > 0:
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
  else:
    # if growtopia hasn't launched in time waits 4 seconds
    time.sleep(4)
    set_screen()
    return


def start():
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
  # x button
  pyautogui.click(
    x=LEFT + SCREEN_WIDTH *0.93,
    y=TOP + SCREEN_HEIGTH*0.1,
    duration=0.5
  )

  time.sleep(3)
  # Survey popup
  # Survey disabled because its completed
  # close_popup()
  time.sleep(1)

  # enter world
  enter_world()

  time.sleep(10)
  # fix_zoom_lvl()

  logger.add_log("Harvester ready")


def go_to_row(row: int):
  pyautogui.keyDown(RIGHT_KS)
  time.sleep(DOOR_TO_FIRST_S)
  pyautogui.keyUp(RIGHT_KS)
  time.sleep(0.5)
  if 1 < row <= 21:
    for _ in range(1, row):
      pyautogui.keyDown(JUMP_KS)
      time.sleep(1.5)
      pyautogui.keyUp(JUMP_KS)
  elif row == 1:
    pass
  else:
    logger.add_log("Something went wrong [TRIED TO GO TO A ROW THAT DOES NOT EXIST]")

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