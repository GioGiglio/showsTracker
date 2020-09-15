import requests
import db

class Show:
  def __init__(self,name,id):
    __slots__ = ['name','id','seasons']
    self.name = name
    self.id = id
    self.seasons = []

  def addSeason(self,s):
    self.seasons.append(s)

class Season:
  def __init__(self,number,id):
    __slots__ = ['number','id','episodes']
    self.number = number
    self.id = id
    self.episodes = []

  def addEpisode(self,e):
    self.episodes.append(e)

class Episode:
  def __init__(self,name, number, id):
    __slots__ = ['name','number','id']
    self.name = name
    self.number = number
    self.id = id

baseUrl = 'http://api.tvmaze.com'


def searchShow(name):
  subUrl = '/search/shows'
  queryUrl = baseUrl + subUrl + '?q=:' + name
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)

  shows = resp.json()

def getShowEpisodes(show):
  queryUrl = '{}/shows/{}/episodes'.format(baseUrl, show.id)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)

  episodes = resp.json()
  curr = 0

  for e in episodes:

    if e['season'] != show.seasons[curr].number:
      # go to next season
      curr += 1
    
    show.seasons[curr].addEpisode(Episode(e['name'], e['number'], e['id']))
  
def getShowSeasons(show):
  queryUrl = '{}/shows/{}/seasons'.format(baseUrl, show.id)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)

  seasons = resp.json()
  for s in seasons:
    show.addSeason(Season(s['number'], s['id']))

def getSeasonEpisodes(seasonId):
  queryUrl = '{}/seasons/{}/episodes'.format(baseUrl, seasonId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)

  print(resp.json())


theOffice = Show('The Office', 526)
getShowSeasons(theOffice)
getShowEpisodes(theOffice)

rickAndMorty = Show('Rick and Morty', 216)
getShowSeasons(rickAndMorty)
getShowEpisodes(rickAndMorty)

# searchShow('')
# getShowSeasons(526)
# getSeasonEpisodes(2087)

for s in rickAndMorty.seasons:
  print('Season: {} id:{}'.format(s.number, s.id))
  for e in s.episodes:
    print('\tEpisode {}: {} id:{}'.format(e.number, e.name, e.id))

db.init()
db.saveShow(rickAndMorty)

