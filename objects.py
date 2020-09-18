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

  def lastNextEpisode(self):
    last = next = None

    for s in self.seasons:
      for e in s.episodes:
        if e.watched:
          last = e
          last.season = s.number
        else:
          break
    return last


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
  def __init__(self,name, number, id, watched=False, season=None):
    __slots__ = ['name','number','id','watched']
    self.name = name
    self.number = number
    self.id = id
    self.watched = watched
    self.season = season

  def __str__(self):
    return 'S{} E{}: {}'.format(
            '0' + str(self.season) if self.season < 10 else self.season,
            '0' + str(self.number) if self.number < 10 else self.number,
            self.name
    )

