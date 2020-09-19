from objects import Show,Episode
import sqlite3
import time
import itertools

DB_PATH = 'showsTracker.db'
conn = None

def __connect():
  return sqlite3.connect(DB_PATH)

def disconnect():
  conn.close()

def init():
  global conn
  conn = __connect()


def checkShowExist(showId):
  curs = conn.cursor()
  curs.execute('SELECT * FROM show WHERE id=?',(showId,))
  return curs.fetchone() != None

def getShowLike(showName):
  curs = conn.cursor()
  showName = showName.replace(' ', '%')
  curs.execute('SELECT id, name FROM show WHERE name LIKE ?', (showName, ))
  s = curs.fetchone()
  return Show(s[0], s[1]) if s else None

def saveShow(show):
  curs = conn.cursor()
  unixTime = int(time.time())
  
  # insert show
  curs.execute('INSERT INTO show VALUES(?,?,?)', (show.id, show.name, unixTime) )

  # insert episodes
  episodes = [(e.id, show.id, e.season, e.number, e.name, 0) for e in show.episodes]
  curs.executemany('INSERT INTO episode VALUES(?,?,?,?,?,?)', episodes)
  conn.commit()

def getShowEpisodes(showId):
  curs = conn.cursor()
  
  query = '''
  SELECT e.id, e.season, e.number, e.name, e.watched
  FROM episode AS e JOIN show ON show.id = e.show_id WHERE e.show_id = ?
  '''

  curs.execute(query, (showId,) )
  
  rows = curs.fetchall()
  episodes = [Episode(r[0], r[1], r[2], r[3], r[4]) for r in rows]
  return episodes

def getShows():
  curs = conn.cursor()

  query = '''
  SELECT s.id, s.name, e.id, e.season, e.number, e.name, e.watched
  FROM show AS s JOIN episode AS e ON s.id = e.show_id ORDER BY s.date_tracked
  '''

  shows = []
  getShowIdLambda = lambda e: e[0]

  curs.execute(query)
  data = curs.fetchall()
  
  # split data to get a list for each show
  for k, g in itertools.groupby(data, getShowIdLambda):
    g = list(g)
    show = Show(g[0],g[1])
    episodes = [Episode(e[2],e[3],e[4],e[5],e[6]) for e in g]
    show.addEpisodes(episodes)
    shows.append(show)

  return shows

