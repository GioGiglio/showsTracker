import requests
import json

class TvShow:
  def __init__(self,name,id):
    __slots__ = ['name','id','seasons']
    self.name = name
    self.id = id
    self.seasons = []

class Season:
  def __init__(self,number,id):
    __slots__ = ['number','id','episodes']
    self.number = number
    self.id = id
    self.episodes = []

class Episode:
  def __init__(self,name, number, id):
    __slots__ = ['name','number','id']
    self.name = name
    self.number = number
    self.id = id

  def __str__(self):
    return 'Id: {} \tNumber: {}\tName: {}'.format(self.id, self.number, self.name)

baseUrl = 'http://api.tvmaze.com'


def searchShow(name):
  subUrl = '/search/shows'
  queryUrl = baseUrl + subUrl + '?q=:' + name
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)

  print(resp.json())

def getShowEpisodes(showId):
  queryUrl = '{}/shows/{}/episodes'.format(baseUrl,showId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)

  episodes = resp.json()
  listOfEpisodes = []
  for e in episodes:
    ep = Episode(e['name'], e['number'], e['id'])
    listOfEpisodes.append(ep)
  
  for e in listOfEpisodes:
    print(e)

def getShowSeasons(ShowId):
  queryUrl = '{}/shows/{}/seasons'.format(baseUrl, ShowId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)



def getSeasonEpisodes(seasonId):
  queryUrl = '{}/seasons/{}/episodes'.format(baseUrl, seasonId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    print('error requesting:', queryUrl)

  print(resp.json())


# searchShow('office')
# getShowSeasons(526)
# getSeasonEpisodes(2087)
getShowEpisodes(526)
