import datetime
import logging
import logging.handlers
import os
import sys


class Logger():

  def __init__(self):
    self.__handler = logging.handlers.WatchedFileHandler(
      "./bot.log"
    )
    self.__formatter = logging.Formatter(logging.BASIC_FORMAT)
    self.__handler.setFormatter(self.__formatter)
    self.__root = logging.getLogger()
    self.__root.setLevel(logging.INFO)
    self.__root.addHandler(self.__handler)

  def add_log(self, message: str):
    logging.info(f"{message} {str(datetime.datetime.now())[:-7]}")
  
  def print_log(self):
    with open("./bot.log", 'r') as f:
      contents = f.readlines()
    for log in contents:
      print(f"{log[:5]} {log[10:-1]}")

  def _remove_log(self):
    if os.path.exists('bot.log'):
      with open('./bot.log', 'w') as f:
        f.write("")

if __name__ == "__main__":
  logger = Logger()
  if len(sys.argv) > 1:
    if sys.argv[1] == "-r" or sys.argv[1] == "--remove":
      logger._delete_log()
  else:
    logger.print_log()
