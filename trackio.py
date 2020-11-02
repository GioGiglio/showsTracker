#!/usr/bin/env python3

from colors import reverse, blue
import db
import reqs
import util
from objects import *
import argparse
import os
import re
import prefs as prefs_mod


def main():
  prefs = prefs_mod.load()
  args = parseArgs()
  os.system('clear')

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
    showEpisodes(args.episodes, prefs['eps_list_summary'])
  elif args.delete:
    db.init()
    deleteShow(args.delete)
  elif args.reset:
    db.init()
    resetShow(args.reset)
  else:
    db.init()
    getShow(args.show, prefs['view'], prefs['curr_next_summary'])

  db.disconnect()
  exit()

def parseArgs():
  parser = argparse.ArgumentParser(description='Shows progress tracker.')
  # if no flag is provided, args are stored in the "show" argument.
  parser.add_argument('show', action='store', nargs='*')
  
  # arg used to track a new tv show
  parser.add_argument('-add',   '-a', action='store', nargs='*')

  # arg used to watch some episodes of the selected tv show
  parser.add_argument('-watch', '-w', action='store', nargs='*')

  # arg used with the "-watch" arg, to select how many episodes to watch
  parser.add_argument('-count', '-c', action='store')
  
  # arg used to print all episodes of the selected tv show
  parser.add_argument('-episodes', '-e', action='store', nargs='*')
  
  # arg used to delete the selected tv show
  parser.add_argument('-delete', action='store', nargs='*')

  # arg used to reset the tracking progress for the selected show
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

  # regex to match html tags
  htmlTagsRe = re.compile('<.*?>')
  
  episodes = reqs.getShowEpisodes(show.id)

  episodes = [ Episode(
                       e['id'],
                       e['season'],
                       e['number'],
                       e['name'],
                       False,       # watched
                       re.sub(htmlTagsRe,'',e['summary']) if e['summary'] else None
                       )
  for e in episodes]
  show.addEpisodes(episodes)
  
  db.saveShow(show)
  print('-- Show saved')

def getShow(name, view, currNextSummary):
  if not name:
    # no show specified, print all shows tracked
    shows = db.getShows()

    if view == 'watching':
      # count not started shows and finished shows
      notStarted = sum(not s.episodes[0].watched for s in shows)
      finished = sum(s.episodes[-1].watched for s in shows)

      # print top message
      print(reverse(' - TRACKED SHOWS - '))
      print(blue('{} to start, {} finished \n'.format(notStarted, finished)))
      # filter only shows started and not finished
      shows = [ s for s in shows if s.episodes[0].watched and not s.episodes[-1].watched ]
    else:
      # view == 'all'
      # print top message
      print(reverse(' - TRACKED SHOWS - \n'))

    for s in shows:
      s.printLastNextEpisodes(currNextSummary)
    
    return

  show = db.getShowLike(' '.join(name))
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

def showEpisodes(args, prefSummary):
  show = db.getShowLike(' '.join(args))
  if not show:
    print('-- Error: Show is not tracked')
    return

  # get show episodes
  episodes = db.getShowEpisodes(show.id)
  show.addEpisodes(episodes)

  print(reverse(' - SHOW EPISODES: {} - \n'.format(show.name)))
  show.printEpisodes(prefSummary)

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

