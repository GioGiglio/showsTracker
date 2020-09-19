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

# TODO fix
  def lastNextEpisode(self):
    lastEp = nextEp = None
    for e in self.episodes:
      if e.watched:
        lastEp = e
      else:
        nextEp = e
        break
      return (lastEp,nextEp)


  def printEpisodes(self):
    for e in self.episodes:
      print('{} S{} E{}: {}'.format(
            '\033[0;32m<o>\033[0m' if e.watched else '\033[1;31m<x>\033[0m',
            e.season, e.number, e.name
      ))

class Episode:
  def __init__(self, id, season, number, name,  watched=False):
    __slots__ = ['id','season','number','name','watched']
    self.id = id
    self.season = season
    self.number = number
    self.name = name
    self.watched = watched

  def __str__(self):
    return 'S{} E{}: {}'.format(
            '0' + str(self.season) if self.season < 10 else self.season,
            '0' + str(self.number) if self.number < 10 else self.number,
            self.name
    )

