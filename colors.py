PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
REVERSE = '\033[;7m'
END = '\033[0m'

def bold(s):
  """Return s in bold"""
  return BOLD + s + END

def red(s):
  """Return s in color red"""
  return RED + s + END

def yellow(s):
  """Return s in color yellow"""
  return YELLOW + s + END

def reverse(s):
  """Return s in reverse style"""
  return REVERSE + s + END
