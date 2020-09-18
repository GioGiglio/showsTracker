import threading
import curses

class UI:
  def __init__(self):
    self.titlebar = None
    self.status = None
    self.side = None
    
    self.setup_curses()
    self.init()

  def setup_curses(self):
    self.win = curses.initscr()

  def init(self):
    self.win.keypad(1)
    
    curses.cbreak()
    curses.noecho()

