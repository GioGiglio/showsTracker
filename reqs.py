from __future__ import annotations
import requests

baseUrl = 'http://api.tvmaze.com'

def searchShow(name: str):
  subUrl = '/search/shows'
  queryUrl = baseUrl + subUrl + '?q=:' + name
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  return resp.json()


def getShowEpisodes(showId: int):
  queryUrl = '{}/shows/{}/episodes'.format(baseUrl, showId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  return resp.json()

def getShowSeasons(showId: int):
  queryUrl = '{}/shows/{}/seasons'.format(baseUrl, showId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  return resp.json()

def getSeasonEpisodes(seasonId: int):
  queryUrl = '{}/seasons/{}/episodes'.format(baseUrl, seasonId)
  resp = requests.get(queryUrl)
  if resp.status_code != 200:
    raise Exception('Request error')

  print(resp.json())

