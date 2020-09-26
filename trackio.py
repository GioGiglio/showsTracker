#!/usr/bin/env python3

from colors import reverse
import db
import reqs
import util
from objects import *
import argparse
import os

def main():
  os.system('clear')
  args = parseArgs()
 
  if args.add:
    db.init()
    addShow(args.add)

  elif args.watch:
    if not args.count:
      db.init()
      watchShow(args.watch)
    else:
      try:
        count = int(args.count)
        if count < 1 or count > 10:
          raise ValueError()
      except ValueError:
        print('-- Error: Invalid count')
        exit(1)
      else:
        db.init()
        watchShow(args.watch, count)
  elif args.episodes:
    db.init()
    showEpisodes(args.episodes)
  elif args.delete:
    db.init()
    deleteShow(args.delete)
  elif args.reset:
    db.init()
    resetShow(args.reset)
  else:
    db.init()
    getShow(args.show)

  db.disconnect()
  exit()

def parseArgs():
  parser = argparse.ArgumentParser(description='Shows progress tracker.')
  parser.add_argument('show', action='store', nargs='*')
  parser.add_argument('-add',   '-a', action='store', nargs='*')
  parser.add_argument('-watch', '-w', action='store', nargs='*')
  parser.add_argument('-episodes', '-e', action='store', nargs='*')
  parser.add_argument('-count', '-c', action='store')
  parser.add_argument('-delete', action='store', nargs='*')
  parser.add_argument('-reset',  action='store', nargs='*')
  return parser.parse_args()
  

def addShow(args):
  print(reverse(' - ADD SHOW - \n'))
  showsData = reqs.searchShow('-'.join(args))
  show = util.promptSelectShow(showsData)
  
  # check if user canceled the action
  if not show:
    print('-- Canceled')
    return

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
    print(reverse(' - TRACKED SHOWS - \n'))
    shows = db.getShows()
    for s in shows:
      s.printLastNextEpisodes()
    
    return

  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- Error: Show is not tracked')
    return

  print(reverse(' - SHOW: {}  - \n'.format(show.name)))
  episodes = db.getShowEpisodes(show.id)
  show.addEpisodes(episodes)
  show.printLastNextEpisodes()

def watchShow(args, count=None):
  show = db.getShowLike(' '.join(args))
  if show:
    episodes = db.getShowEpisodes(show.id)
    show.addEpisodes(episodes)
  else:
    print('-- Error: Show is not tracked')
    return

  print(reverse(' - WATCH EPISODES: {} - \n'.format(show.name)))
  nextEpIdx = show.getNextEpisodeIdx()
  if nextEpIdx is None:
    # show finished, no more episodes to watch
    print('-- Show finished, no more episodes to watch.')
    return
  
  epsIds= util.promptEpisodesToWatch(show, nextEpIdx, count)
  if epsIds is None:
    print('-- Canceled')
    return
  else:
    db.setEpisodesWatched(epsIds, show.id)
    print('-- Episodes marked as watched')

def showEpisodes(args):
  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- Error: Show is not tracked')
    return

  # get show episodes
  episodes = db.getShowEpisodes(show.id)
  show.addEpisodes(episodes)

  print(reverse(' SHOW EPISODES: {} - \n'.format(show.name)))
  show.printEpisodes()

def deleteShow(args):
  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- Error: Show is not tracked')
    return

  print(reverse(' - DELETE SHOW: {} - \n'.format(show.name)))
  if util.confirmDelete(show):
    db.deleteShow(show.id)
    print('-- Show deleted')
  else:
    print('-- Canceled')

def resetShow(args):

  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- Error: Show is not tracked')
    return

  print(reverse(' - RESET SHOW PROGRESS: {} - \n'.format(show.name)))
  if util.confirmReset(show):
    db.resetShow(show.id)
    print('-- Progress reset')
  else:
    print('-- Canceled')


if __name__ == '__main__':
  main()

