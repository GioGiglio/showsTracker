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
    

  def printCurrNextEpisodes(self, prefs):
    '''prefs is the namedtuple OverviewSummary(on, off, onlyWatched)
    '''
    currEp, nextEp = self.getCurrNextEpisodes()
    watched = sum(e.watched for e in self.episodes)
    toWatch = len(self.episodes) - watched
    progressPercentage = int((watched / len(self.episodes)) * 100)
    countInfo = bold(blue(str(progressPercentage) + '%')) + ' (' + bold(blue(str(watched))) + ' | ' + bold(blue(str(toWatch))) + ')'
    print('{}: {}'.format(bold(self.name), countInfo))

    if currEp:
      withSummary = not prefs.off
      currEp.printWithSummary(withSummary)
    else:
      print('No episode watched...')

    if nextEp:
      withSummary = prefs.on
      nextEp.printWithSummary(withSummary)
    else:
      print('No more episodes to watch...')

    print()

  def printEpisodes(self, prefs):
    '''prefs is the namedtuple EpsListSummary(on, off, onlyWatched)
    '''
    if not self.episodes:
      return

    currSeason = self.episodes[0].season
    for e in self.episodes:
      if e.season != currSeason:
        # episode from another season
        currSeason = e.season
        print()

      if e.season == currSeason:
        withSummary = prefs.on or (prefs.onlyWatched and e.watched)
        e.printWithSummary(withSummary)

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

  def printWithSummary(self, withSummary=True):
    eye = bold('<o>') if self.watched else bold(red('<x>'))
    if withSummary:
      space = term_width - 20 - len(self.name)
      summ = gray(italic(self.summary[:space])) if self.summary else ''
      print('{} S{} E{:<2}: {} {}'.format(eye, self.season, self.number, self.name, summ))
    else:
      print('{} S{} E{:<2}: {}'.format(eye, self.season, self.number, self.name))
 
