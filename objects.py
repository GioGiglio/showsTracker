from colors import bold, red, blue, italic, gray
import shutil

# obtain terminal width
term_width = shutil.get_terminal_size()[0]

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

  def getCurrNextEpisodes(self):
    try:
      currEp = next(e for e in reversed(self.episodes) if e.watched)
    except StopIteration:
      currEp = None

    try:
      nextEp = next(e for e in self.episodes if not e.watched)
    except StopIteration:
      nextEp = None
      
    return (currEp, nextEp)

  def getNextEpisodeIdx(self):
    try:
      nextEpIdx = next(i for (i,e) in enumerate(self.episodes) if not e.watched)
    except StopIteration:
      nextEpIdx = None
    
    return nextEpIdx
    

  def printLastNextEpisodes(self, prefCurrNextSummary):
    currEp, nextEp = self.getCurrNextEpisodes()
    watched = sum(e.watched for e in self.episodes)
    toWatch = len(self.episodes) - watched
    progressPercentage = int((watched / len(self.episodes)) * 100)
    countInfo = bold(blue(str(progressPercentage) + '%')) + ' (' + bold(blue(str(watched))) + ' | ' + bold(blue(str(toWatch))) + ')'
    # print('{}: {}\n{}\n{}\n'.format(bold(self.name), countInfo, lastEp, nextEp))
    print('{}: {}'.format(bold(self.name), countInfo))
    if currEp:
      currEp.print(prefCurrNextSummary)
    else:
      print('No episode watched...')

    if nextEp:
      nextEp.print(prefCurrNextSummary)
    else:
      print('No more episodes to watch...')

    print()

  def printEpisodes(self, prefSummary):
    if not self.episodes:
      return

    lastSeason = self.episodes[0].season
    for e in self.episodes:
      if e.season == lastSeason:
        e.print(prefSummary)
      else:
        # episode from another season
        lastSeason = e.season
        print()

class Episode:
  """Describes an episode of a tv show.
  It is contained into a Show object."""

  def __init__(self, id, season, number, name,  watched=False, summary=None):
    __slots__ = ['id','season','number','name','watched', 'summary']
    self.id = id
    self.season = season
    self.number = number
    self.name = name
    self.watched = watched
    self.summary = summary

  def __str__(self):
    space = term_width - 20 - len(self.name)
    return '{} S{} E{:<2}: {} {}'.format(
            bold('<o>') if self.watched else bold(red('<x>')) ,
            self.season, self.number, self.name, gray(italic(self.summary[:space])) if self.summary else ''
    )

  def print(self, prefSummary):
    space = term_width - 20 - len(self.name)

    ep = '{} S{} E{:<2}: {}'.format(
      bold('<o>') if self.watched else bold(red('<x>')) ,
      self.season, self.number, self.name)

    if prefSummary == 'off':
      print(ep)
    elif prefSummary == 'on':
      summ = gray(italic(self.summary[:space])) if self.summary else ''
      print(ep, summ)
    elif prefSummary == 'only_watched':
      if not self.watched:
        print(ep)
      else:
        summ = gray(italic(self.summary[:space])) if self.summary else ''
        print(ep, summ)


