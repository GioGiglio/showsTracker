import requests
import db
from objects import *

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

 #theOffice.printEpisodes()
 #rickAndMorty.printEpisodes()

# searchShow('')
# getShowSeasons(526)
# getSeasonEpisodes(2087)
#db.getShows()
#db.saveShow(rickAndMorty)


db.init()
shows = db.getShows()
for s in shows:
  s.printEpisodes()
