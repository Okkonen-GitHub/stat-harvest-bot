import datetime
import logging
import logging.handlers


class Logger():

  def __init__(self):
    self.handler = logging.handlers.WatchedFileHandler(
      "./bot.log"
    )
    self.formatter = logging.Formatter(logging.BASIC_FORMAT)
    self.handler.setFormatter(self.formatter)
    self.root = logging.getLogger()
    self.root.setLevel(logging.INFO)
    self.root.addHandler(self.handler)

  def add_log(self, message: str):
    logging.info(f"{message} {str(datetime.datetime.now())[:-7]}")
  
  def print_log(self):
    with open("./bot.log", 'r') as f:
      contents = f.readlines()
    for log in contents:
      print(f"{log[:5]} {log[10:-1]}")

if __name__ == "__main__":
  Logger().print_log()
