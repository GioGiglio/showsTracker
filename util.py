from objects import *
import re

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def bold(s):
  return color.BOLD + s + color.END

def red(s):
  return color.RED + s + color.END

def promptSelectShow(showsData):
  # regex to match html tags
  htmlTagsRe = re.compile('<.*?>')
  
  i = 0
  for s in showsData[:5]:

    s = s['show']

    # remove html tags from summary
    summaryText = re.sub(htmlTagsRe, '', s['summary'][:200]) if s['summary'] else ''

    print('#{}\nName: {}\nGenres: {}\nSummary: {}...\n'.format(
          i,
          s['name'],
          ", ".join(s['genres']),
          summaryText
    ))
    i += 1

  while True:
    try:
      selected = int(input('Select the show: #'))
      if selected < 0 or selected >= i:
        raise ValueError()
      break
    except ValueError:
      print('Invalid selection!')

  id = showsData[selected]['show']['id']
  name = showsData[selected]['show']['name']
  return Show(id, name)

