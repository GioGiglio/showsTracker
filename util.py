from objects import *
from colors import bold, reverse, yellow
import re
import os

def __confirmEpisodesToWatch(show, nextIdx, count, end):
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


def promptEpisodesToWatch(show, nextIdx, count):
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
    print(reverse(' - WATCH EPISODES: {} - \n'.format(show.name)))
    epsIds = __confirmEpisodesToWatch(show,nextIdx,count,end)
    return epsIds

def promptSelectShow(showsData):
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
      selected = int(input('Select show: # '))
      if selected == -1:
        return None

      if selected < 0 or selected >= i:
        raise ValueError()
      break
    except ValueError:
      print('-- Invalid selection. [ -1 to cancel the operation ].')

  id = showsData[selected]['show']['id']
  name = showsData[selected]['show']['name']
  return Show(id, name)

def confirmReset(show):
  """Ask the user to confirm the reset of watching progress for the show.
  """
  
  print('Do you really want to RESET the progress for {}? (Cannot be undone) [yes/no]: '.format(bold(show.name)), end='')
  while True:
    choice = input()
    if choice == 'yes':
      return True
    if choice == 'no':
      return False
    else:
      print('Invalid choice. Please select either yes or no: ', end='')
  
def confirmDelete(show):
  """Ask the user to confirm the deletion of a show and its progress.
  """
  
  print('Do you really want to DELETE the show {} and its progress? (Cannot be undone) [yes/no]: '.format(bold(show.name)), end='')
  while True:
    choice = input()
    if choice == 'yes':
      return True
    if choice == 'no':
      return False
    else:
      print('Invalid choice. Please select either yes or no: ', end='')
