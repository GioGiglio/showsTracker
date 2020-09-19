#!/usr/bin/env python3

import db
import reqs
import util
from objects import *
import threading
import argparse
import os

# Shows: Rick and Morty, Peaky blinders, The office, Futurama

def main():
  os.system('clear')
  db.init()
  args = parseArgs()
  print(args)


  shows = db.getShows()
  for s in shows:
    print(s.lastNextEpisode())

  db.disconnect()
  exit()
  
  if args.add:
    addShow(args.add)
  elif args.show:
    getShow(args.show)

    
  db.disconnect()
  exit()

# TODO add argument to watch n episodes
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
  
  episodes = reqs.getShowEpisodes(show.id)
  episodes = [ Episode(e['id'], e['season'], e['number'], e['name']) for e in episodes]
  show.addEpisodes(episodes)
  
  db.saveShow(show)
  show.printEpisodes()


def getShow(args):
  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- ERROR: Show is not tracked')
    return

  episodes = db.getShowEpisodes(show.id)
  show.addEpisodes(episodes)
  show.printEpisodes()
  
  #print(show.lastWatchedEpisode())
  #show.printEpisodes()

if __name__ == '__main__':
  main()


 #theOffice = Show(526, 'The Office')
 #rickAndMorty = Show(216, 'Rick and Morty')
