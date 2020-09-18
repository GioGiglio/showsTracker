class Show:
  def __init__(self,name,id):
    __slots__ = ['name','id','seasons']
    self.name = name
    self.id = id
    self.seasons = []

  def addSeason(self,s):
    self.seasons.append(s)
  
  def addSeasons(self, seasons):
    self.seasons.extend(seasons)

  def printEpisodes(self):
    for s in self.seasons:
      print('Season: {}'.format(s.number))
      for e in s.episodes:
        print('\tEpisode {}: {}'.format(e.number, e.name))

class Season:
  def __init__(self,number,id):
    __slots__ = ['number','id','episodes']
    self.number = number
    self.id = id
    self.episodes = []

  def addEpisode(self,e):
    self.episodes.append(e)

class Episode:
  def __init__(self,name, number, id, watched=False):
    __slots__ = ['name','number','id','watched']
    self.name = name
    self.number = number
    self.id = id
    self.watched = watched

