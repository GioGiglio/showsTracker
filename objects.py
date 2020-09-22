from util import bold,red

class Show:
  def __init__(self,id, name):
    __slots__ = ['id','name','episodes']
    self.id = id
    self.name = name
    self.episodes = []

  def addEpisode(self,e):
    self.episodes.append(e)
  
  def addEpisodes(self, episodes):
    self.episodes.extend(episodes)

  def getLastNextEpisodes(self):
    try:
      lastEp = next(e for e in reversed(self.episodes) if e.watched)
    except StopIteration:
      lastEp = None

    try:
      nextEp = next(e for e in self.episodes if not e.watched)
    except StopIteration:
      nextEp = None
      
    return (lastEp, nextEp)

  def printLastNextEpisodes(self):
    lastEp, nextEp = self.getLastNextEpisodes()
    lastEp = 'No episode watched...' if lastEp is None else lastEp
    nextEp = 'No more episodes to watch' if nextEp is None else nextEp
    print('{}:\n{}\n{}\n'.format(bold(self.name), lastEp, nextEp))

  def nextEpisode(self):
    return next(e for e in self.episodes if not e.watched)

  def printEpisodes(self):
    print(*self.episodes, sep='\n') 

class Episode:
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

#    return 'S{} E{}: {}'.format(
#            '0' + str(self.season) if self.season < 10 else self.season,
#            '0' + str(self.number) if self.number < 10 else self.number,
#            self.name
#    )

