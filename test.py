import json
from objects import Show, Episode

def save(shows):
  out = []
  for s in shows:
    d = vars(s)
    d['episodes'] = [vars(x) for x in s.episodes]
    out.append(d)
    
  with open('shows.json','w') as f:
    f.write(json.dumps(out))


def read():
  with open('shows.json','r') as f:
    data = json.load(f)
    shows = [Show(x['id'], x['name']) for x in data]
    i = 0
    for s in data:
      eps = [Episode(x['id'],x['season'],x['number'],x['name'],x['watched'],x['summary']) for x in s['episodes']]
      shows[i].addEpisodes(eps)
      i+=1
  
  for s in shows:
    s.printLastNextEpisodes('only_watched')

