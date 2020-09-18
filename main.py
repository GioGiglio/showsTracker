import db
import reqs
import util
from objects import *
import threading
import argparse
import os

def main():
  os.system('clear')
  db.init()
  args = parseArgs()
  print(args)
  
  if args.add:
    addShow(args.add)
  elif args.show:
    getShow(args.show)

    
  db.disconnect()
  exit()

def parseArgs():
  parser = argparse.ArgumentParser(description='Shows progress tracker.')
  parser.add_argument('-add', action='store', nargs='*')
  parser.add_argument('show', action='store', nargs='*')
  parser.add_argument('-watch', action='store', nargs='*')
  return parser.parse_args()
  

def addShow(args):
  showsData = reqs.searchShow('-'.join(args))
  show = util.promptSelectShow(showsData)

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


def getShow(args):
  print(args)
  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- ERROR: Cannot find show')
    return
  
  show = db.getShow(show.id)
  print(show.lastWatchedEpisode())
  #show.printEpisodes()

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

