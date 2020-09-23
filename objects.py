from __future__ import annotations
from typing import List, Tuple, Optional
from util import bold,red

class Show:
  def __init__(self,id, name):
    __slots__ = ['id','name','episodes']
    self.id = id
    self.name = name
    self.episodes = []

  def addEpisode(self, e: Episode):
    self.episodes.append(e)
  
  def addEpisodes(self, episodes: List[Episode]):
    self.episodes.extend(episodes)

  def getLastNextEpisodes(self) -> Tuple[Optional[Episode], Optional[Episode]]:
    try:
      lastEp = next(e for e in reversed(self.episodes) if e.watched)
    except StopIteration:
      lastEp = None

    try:
      nextEp = next(e for e in self.episodes if not e.watched)
    except StopIteration:
      nextEp = None
      
    return (lastEp, nextEp)

  def getNextEpisodeIdx(self) -> Optional[int]:
    try:
      nextEpIdx = next(i for (i,e) in enumerate(self.episodes) if not e.watched)
    except StopIteration:
      nextEpIdx = None
    
    return nextEpIdx
    

  def printLastNextEpisodes(self):
    lastEp, nextEp = self.getLastNextEpisodes()
    lastEp = 'No episode watched...' if lastEp is None else lastEp
    nextEp = 'No more episodes to watch' if nextEp is None else nextEp
    print('{}:\n{}\n{}\n'.format(bold(self.name), lastEp, nextEp))

  def printEpisodes(self):
    print(*self.episodes, sep='\n') 

class Episode:
  """Describes an episode of a tv show.
  It is contained into a Show object."""

  def __init__(self, id, season, number, name,  watched=False):
    __slots__ = ['id','season','number','name','watched']
    self.id = id
    self.season = season
    self.number = number
    self.name = name
    self.watched = watched

  def __str__(self):
    return '{} S{} E{}: {}'.format(
            bold('<o>') if self.watched else bold(red('<x>')) ,
            self.season, self.number, self.name
    )

