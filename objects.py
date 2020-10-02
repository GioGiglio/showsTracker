from colors import bold, red, blue

class Show:
  def __init__(self,id, name):
    __slots__ = ['id','name','episodes']
    self.id = id
    self.name = name
    self.episodes = []

  def addEpisode(self, e):
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

  def getNextEpisodeIdx(self):
    try:
      nextEpIdx = next(i for (i,e) in enumerate(self.episodes) if not e.watched)
    except StopIteration:
      nextEpIdx = None
    
    return nextEpIdx
    

  def printLastNextEpisodes(self):
    lastEp, nextEp = self.getLastNextEpisodes()
    lastEp = 'No episode watched...' if lastEp is None else lastEp
    nextEp = 'No more episodes to watch' if nextEp is None else nextEp
    watched = sum(e.watched for e in self.episodes)
    toWatch = len(self.episodes) - watched
    countInfo = bold(blue(str(watched))) + ' | ' + bold(blue(str(toWatch)))
    #countInfo = blue('<o> ' + str(watched)) + ' | ' + blue('<x> ' + str(toWatch))
    print('{}: {}\n{}\n{}\n'.format(bold(self.name), countInfo, lastEp, nextEp))

  def printEpisodes(self):
    if not self.episodes:
      return

    lastSeason = self.episodes[0].season
    for e in self.episodes:
      if e.season != lastSeason:
        lastSeason = e.season
        print()
      print(e)

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
    return '{} S{} E{:<2}: {}'.format(
            bold('<o>') if self.watched else bold(red('<x>')) ,
            self.season, self.number, self.name
    )

