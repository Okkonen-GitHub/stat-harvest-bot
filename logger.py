import logging

class Logger():

  def __init__(self):
    self.log = logging.getLogger("harvest_log")

  def completed(self):
    pass
