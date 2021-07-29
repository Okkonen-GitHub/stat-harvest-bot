import logging
import logging.handlers
import datetime


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
    logging.info(message)

if __name__ == "__main__":
  log = Logger()
  log.add_log(f"TEST {str(datetime.datetime.now())[:-7]}")