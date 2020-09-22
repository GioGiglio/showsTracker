#!/usr/bin/env python3

import db
import reqs
import util
from objects import *
import argparse
import os

def main():
  os.system('clear')
  db.init()
  args = parseArgs()
  print(args)
 
  if args.add:
    addShow(args.add)

  elif args.watch:
    watchShow(args.watch)
  
  else:
    getShow(args.show)

  db.disconnect()
  exit()

# TODO add argument to watch n episodes
def parseArgs():
  parser = argparse.ArgumentParser(description='Shows progress tracker.')
  parser.add_argument('-add', action='store', nargs='*')
  parser.add_argument('-next', action='store', nargs='*')
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
  
  episodes = reqs.getShowEpisodes(show.id)
  episodes = [ Episode(e['id'], e['season'], e['number'], e['name']) for e in episodes]
  show.addEpisodes(episodes)
  
  db.saveShow(show)
  print('-- Show saved')

def getShow(args):
  if not args:
    # no show specified, print all shows tracked
    shows = db.getShows()
    for s in shows:
      s.printLastNextEpisodes()
    
    return

  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- ERROR: Show is not tracked')
    return

  episodes = db.getShowEpisodes(show.id)
  show.addEpisodes(episodes)
  show.printLastNextEpisodes()
  
  #print(show.lastWatchedEpisode())
  #show.printEpisodes()

# args can be:
# showstracker -watch the office -count 2
# showstracker -watch the office -e 2 (RECCOMENDED)
# showstracker -watch the office -n 2
# showstracker -watch 2 of the office (NOT RECCOMENDED)
def watchShow(args):
  print('todo')

  # ask for confirm before

if __name__ == '__main__':
  main()

