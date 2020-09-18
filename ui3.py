import curses
import curses.ascii

class Ui:
  def __init__(self):
    self.stdscr = curses.initscr()
    self.stdscr.keypad(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    
    # windows
    h,w = self.stdscr.getmaxyx()
    self.sidewin = curses.newwin(h-1, w//3, 0, w - w//3)
    self.cmdwin = curses.newwin(1, w, h-1, 0)
  
    # logic
    self.stdscr.refresh()
  
    self.sidewin.addstr(1,1,'Side Window')
    self.sidewin.border('|',' ',' ',' ','|',' ','|',' ')
    self.sidewin.refresh()
  
    self.cmdwin.addstr(0,0,'THIS IS THE LAST LINE --- STATUS BAR -----', curses.A_BOLD)
    self.cmdwin.refresh()

  def start(self):
    while 1:
      self.stdscr.refresh()
      self.cmdwin.getch()
    
  def cmdWrite(self,s):
    self.cmdwin.erase()
    self.cmdwin.addstr(0,0,s,curses.A_BOLD)
    self.cmdwin.refresh()

  def cmdAdd(self,s):
    self.cmdwin.insstr(s,curses.A_BOLD)
    self.cmdwin.refresh()

  def printShowsList(self,shows):
    # Shows are always displayed on stdscr
    print('ok')  

  def printShows(self, shows):
    #self.stdscr.erase()
    for i,s in enumerate(shows):
      self.stdscr.addstr(i+1, 1, s.name)

    self.stdscr.refresh()
    self.stdscr.getch()

def sub():
  currwin = stdscr
  while 1:
    c = currwin.getch()
    if c == ord('a'):
      currwin.addstr(1,3,'A pressed')
    elif c == ord('r'):
      currwin.addstr(1,3,'R pressed')
    elif c == ord('s'):
      cmdAdd('NEW STATUS LINE xD xD')
    elif c == curses.ascii.ESC:
      currwin.addstr(1,3,'ESC pressed')
    elif c == ord('l'):
      # left key
      if currwin == stdscr:
        currwin = sidewin;
    elif c == ord('h'):
      # right key
      if currwin == sidewin:
        currwin = stdscr
    elif c == ord('q'):
      break

