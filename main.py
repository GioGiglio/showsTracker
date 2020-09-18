import db
from ui3 import Ui
from objects import *
import threading
import argparse
import os
import reqs
import re

# globals

def main():
  os.system('clear')
  db.init()
  args = parseArgs()
  print(args)
  
  if args.add:
    addShow(args.add)

  db.disconnect()
  exit()

def parseArgs():
  parser = argparse.ArgumentParser(description='Shows progress tracker.')
  parser.add_argument('-add', action='store', nargs='*')
  # parser.add_argument('-watch', action='store', nargs='*')
  return parser.parse_args()
  

def addShow(args):
  showsData = reqs.searchShow('-'.join(args))
  show = promptSelectShow(showsData)

  # if show already exist in database, skip
  if db.checkShowExist(show.id):
    print('-- Show already tracked')
    return
  
  seasons = reqs.getShowSeasons(show.id)
  seasons = [ Season(s['number'], s['id']) for s in seasons]
  show.addSeasons(seasons)

  episodes = reqs.getShowEpisodes(show.id)
  curr = 0
  for e in episodes:
    if e['season'] != show.seasons[curr].number:
      # go to next season
      curr += 1
    
    # add episode to current season
    show.seasons[curr].addEpisode(Episode(e['name'], e['number'], e['id']))

  db.saveShow(show)
  show.printEpisodes()

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
  return Show(name, id)

if __name__ == '__main__':
  main()


 #theOffice = Show('The Office', 526)
 #getShowSeasons(theOffice)
 #getShowEpisodes(theOffice)
 #
 #rickAndMorty = Show('Rick and Morty', 216)
 #getShowSeasons(rickAndMorty)
 #getShowEpisodes(rickAndMorty)
 #
  ##theOffice.printEpisodes()
  ##rickAndMorty.printEpisodes()
 #
 ## searchShow('')
 ## getShowSeasons(526)
 ## getSeasonEpisodes(2087)
 ##db.getShows()
 ##db.saveShow(rickAndMorty)
 #
 #ui = Ui()
 #uiThread = threading.Thread(target=ui.start())
 #
 #db.init()
 #shows = db.getShows()
 #
 #ui.printShows(shows)
 #
 ##for s in shows:
 ##  s.printEpisodes()

