import requests

baseUrl = 'http://api.tvmaze.com'

def searchShow(name):
  subUrl = '/search/shows'
  queryUrl = baseUrl + subUrl + '?q=:' + name
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  return resp.json()


def getShowEpisodes(showId):
  queryUrl = '{}/shows/{}/episodes'.format(baseUrl, showId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  return resp.json()

def getShowSeasons(showId):
  queryUrl = '{}/shows/{}/seasons'.format(baseUrl, showId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  return resp.json()
  for s in seasons:
    show.addSeason(Season(s['number'], s['id']))

def getSeasonEpisodes(seasonId):
  queryUrl = '{}/seasons/{}/episodes'.format(baseUrl, seasonId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  print(resp.json())

