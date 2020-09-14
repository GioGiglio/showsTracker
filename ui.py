import curses
import curses.ascii

def cmdWrite(s):
  cmdwin.erase()
  cmdwin.addstr(0,0,s,curses.A_BOLD)
  cmdwin.refresh()

def cmdAdd(s):
  cmdwin.insstr(s,curses.A_BOLD)
  cmdwin.refresh()

def printShowsList(shows):
  # Shows are always displayed on stdscr
  print('ok')  

# init
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.curs_set(0)

# windows
h,w = stdscr.getmaxyx()
sidewin = curses.newwin(h-1, w//3, 0, w - w//3)
cmdwin = curses.newwin(1, w, h-1, 0)

# logic
stdscr.refresh()

sidewin.addstr(1,1,'Side Window')
sidewin.border('|',' ',' ',' ','|',' ','|',' ')
sidewin.refresh()

cmdwin.addstr(0,0,'THIS IS THE LAST LINE --- STATUS BAR -----', curses.A_BOLD)
cmdwin.refresh()

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

