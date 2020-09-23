from __future__ import annotations
from typing import List
from objects import *
import re
import os

class color:
  """Utility class that collects the escape sequences
  for printing colored or styled text.
  """
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


def bold(s) -> str:
  """Return s in bold"""
  return color.BOLD + s + color.END

def red(s) -> str:
  """Return s in color red"""
  return color.RED + s + color.END

def yellow(s) -> str:
  """Return s in color yellow"""
  return color.YELLOW + s + color.END

def __confirmEpisodesToWatch(show, nextIdx, count, end) -> List[int]:
  """Highlight in yellow the episodes to watch
  and prompts the user to confirm the selection
  """
  for (i,e) in enumerate(show.episodes[nextIdx:end]):
    row = '{:>2} | S{} E{} : {}'.format(i+1, e.season, e.number, e.name)
    row = yellow(row) if i < count else row
    print(row)
  
  print()
  while True:
    choice = input('Confirm {} episodes watched? [y/n]: '.format(count))
    if choice in ['','y','yes']:
      break
    if choice in ['n','no']:
      return None

  epsIds = [e.id for e in show.episodes[nextIdx:nextIdx+count]]
  return epsIds


def promptEpisodesToWatch(show, nextIdx, count) -> List[int]:
  """Print the next 10 (or less) episodes to watch
  and prompt the user to select how many episodes to
  mark as watched.
  The __confirmEpisodesToWatch function is called once
  the user selects the number of episodes watched.
  """
  end = nextIdx + 10

  if len(show.episodes) <= end:
    end = (len(show.episodes))
  
  if count:
    return __confirmEpisodesToWatch(show,nextIdx,count,end)

  # no count provided, prompt user 
  else:
    for (i,e) in enumerate(show.episodes[nextIdx:end]):
      print('{:>2} | S{} E{} : {}'.format(i+1, e.season, e.number, e.name))

    print()
    while True:
      try:
        count = input('Episodes watched: ')
        count = int(count)
        if count == -1:
          return None
        if count < 1 or count > 10:
          raise ValueError
      except ValueError:
        print('-- Invalid selection. [ -1 to cancel the operation ]')
      else:
        break
    
    os.system('clear')
    epsIds = __confirmEpisodesToWatch(show,nextIdx,count,end)
    return epsIds

def promptSelectShow(showsData) -> Show:
  """Parse the json data returned from reqs.searchShow(),
  print name, genre and summary for the first 5 shows and
  prompt the user to select one of them.
  """
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

