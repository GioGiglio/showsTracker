import blessed as bl

class UI:
  def __init__(self):
    self.term = bl.Terminal()

    # clear terminal screen
    #print(f"{self.term.home}{self.term.clear}")
    print(self.term.home + self.term.clear)

    self.term.enter_fullscreen()
    print(self.term.blink("Insert System disk into drive A:"))
    print(self.term.green_reverse('master hacker'))
    self.term.inkey()
    self.term.exit_fullscreen()
    
    # fullscreen mode
     #with self.term.fullscreen():
       #print(self.term.blink("Insert System disk into drive A:"))
       #print(self.term.green_reverse('master hacker'))
       #print(self.term.green_underline('master hacker underlined'))
       #self.term.inkey()

