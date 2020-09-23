from __future__ import annotations
from typing import Optional, List
from objects import Show,Episode
import sqlite3
import time
import itertools

DB_PATH = 'showsTracker.db'
conn = None

def __connect() -> sqlite3.Connection:
  return sqlite3.connect(DB_PATH)

def disconnect():
  conn.close()

def init():
  """Initializes the connection to the database.
  """
  global conn
  conn = __connect()


def checkShowExist(showId: int) -> bool:
  """Query the database for a show id to check its existence.
  """
  curs = conn.cursor()
  curs.execute('SELECT * FROM show WHERE id=?',(showId,))
  return curs.fetchone() != None

def getShowLike(showName: str) -> Optional[Show]:
  """Query the database for a show name, using LIKE keyword
  and % instead of spaces.
  """
  curs = conn.cursor()
  showName = showName.replace(' ', '%')
  curs.execute('SELECT id, name FROM show WHERE name LIKE ?', (showName, ))
  s = curs.fetchone()
  return Show(s[0], s[1]) if s else None

def saveShow(show: Show):
  """Inserts a shows and its episodes into the database.
  """
  curs = conn.cursor()
  unixTime = int(time.time())
  
  # insert show
  curs.execute('INSERT INTO show VALUES(?,?,?)', (show.id, show.name, unixTime) )

  # insert episodes
  episodes = [(e.id, show.id, e.season, e.number, e.name, 0) for e in show.episodes]
  curs.executemany('INSERT INTO episode VALUES(?,?,?,?,?,?)', episodes)
  conn.commit()

def getShowEpisodes(showId: int) -> List[Episode]:
  """Query the database for all the episodes of a show.
  """
  curs = conn.cursor()
  
  query = '''
  SELECT e.id, e.season, e.number, e.name, e.watched
  FROM episode AS e JOIN show ON show.id = e.show_id WHERE e.show_id = ?
  '''

  curs.execute(query, (showId,) )
  
  rows = curs.fetchall()
  episodes = [Episode(r[0], r[1], r[2], r[3], r[4]) for r in rows]
  return episodes

def getShows() -> List[Show]:
  """Query the database for every show and its episodes.
  """
  curs = conn.cursor()

  query = '''
  SELECT s.id, s.name, e.id, e.season, e.number, e.name, e.watched
  FROM show AS s JOIN episode AS e ON s.id = e.show_id ORDER BY s.date_tracked DESC
  '''

  shows = []
  getShowIdLambda = lambda e: e[0]

  curs.execute(query)
  data = curs.fetchall()
  
  # split data to get a list for each show
  for k, g in itertools.groupby(data, getShowIdLambda):
    g = list(g)
    show = Show(g[0][0], g[0][1])
    episodes = [Episode(e[2],e[3],e[4],e[5],e[6]) for e in g]
    show.addEpisodes(episodes)
    shows.append(show)

  return shows

def setEpisodesWatched(epsIds: List[int]):
  """Update episodes setting to 1 its watched attribute.
  """
  epsIds = [(e,) for e in epsIds]
  curs = conn.cursor()
  curs.executemany('UPDATE episode SET watched = 1 WHERE id = ?', (epsIds))
  conn.commit()

def resetShow(showId: int):
  curs = conn.cursor()

  query = 'UPDATE episode SET watched = 0 WHERE show_id = ?'
  curs.execute(query, (showId,) )
  conn.commit()

