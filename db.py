from objects import Show,Episode
from pathlib import Path
import sqlite3
import time
import itertools

DB_PATH = '/home/gio/.personal/trackio/trackio.db'
conn = None

def __initDB():
  """Executes sql to create the tables needed.
  """

  createShowTable = '''
  CREATE TABLE IF NOT EXISTS show (
	  id	INTEGER NOT NULL,
	  name	TEXT NOT NULL,
	  date_tracked	INTEGER NOT NULL,
    PRIMARY KEY(id)
  )
  '''

  createEpisodeTable  = '''
  CREATE TABLE IF NOT EXISTS episode (
  	id	INTEGER NOT NULL,
  	show_id	INTEGER NOT NULL,
  	season	INTEGER NOT NULL,
  	number	INTEGER NOT NULL,
  	name	TEXT NOT NULL,
  	watched	INTEGER NOT NULL,
  	summary	TEXT,
  	PRIMARY KEY(id)
  )
  '''
 
  curs = conn.cursor()

  curs.execute(createShowTable)
  curs.execute(createEpisodeTable)
  conn.commit()

def __connect():
  return sqlite3.connect(DB_PATH)

def disconnect():
  conn.close()

def init():
  """Initializes the connection to the database,
  creating and initializing it if it does not exist yet.
  """
  
  global conn
  
  # if the DB file doesn't exists, create the db
  dbFilePath = Path(DB_PATH)
  if not dbFilePath.exists():
    # create .db file first, then connect and create tables
    print('-- info: database does not exist yet. Creating and initializing it...')
    dbFilePath.touch()
    conn = __connect()
    __initDB()
  else:
    conn = __connect()


def checkShowExist(showId):
  """Query the database for a show id to check its existence.
  """
  curs = conn.cursor()
  curs.execute('SELECT * FROM show WHERE id=?',(showId,))
  return curs.fetchone() != None

def getShowLike(showName):
  """Query the database for a show name, using LIKE keyword
  and % instead of spaces.
  """
  curs = conn.cursor()
  showName = showName.replace(' ', '%') + '%'
  curs.execute('SELECT id, name FROM show WHERE name LIKE ?', (showName, ))
  s = curs.fetchone()
  return Show(s[0], s[1]) if s else None

def saveShow(show):
  """Inserts a shows and its episodes into the database.
  """
  curs = conn.cursor()
  unixTime = int(time.time())
  
  # insert show
  curs.execute('INSERT INTO show VALUES(?,?,?)', (show.id, show.name, unixTime) )

  # insert episodes
  episodes = [(e.id, show.id, e.season, e.number, e.name, 0, e.summary) for e in show.episodes]
  curs.executemany('INSERT INTO episode VALUES(?,?,?,?,?,?,?)', episodes)
  conn.commit()

def getShowEpisodes(showId):
  """Query the database for all the episodes of a show.
  """
  curs = conn.cursor()
  
  query = '''
  SELECT e.id, e.season, e.number, e.name, e.watched, e.summary
  FROM episode AS e JOIN show ON show.id = e.show_id WHERE e.show_id = ?
  ORDER BY season, number
  '''

  curs.execute(query, (showId,) )
  
  rows = curs.fetchall()
  episodes = [Episode(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
  return episodes

def getShows():
  """Query the database for every show and its episodes.
  """
  curs = conn.cursor()

  query = '''
  SELECT s.id, s.name, e.id, e.season, e.number, e.name, e.watched, e.summary
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
    episodes = [Episode(e[2],e[3],e[4],e[5],e[6],e[7]) for e in g]
    show.addEpisodes(episodes)
    shows.append(show)

  return shows

def setEpisodesWatched(epsIds, showId):
  """Update episodes setting to 1 its watched attribute.
  Update also the show date_tracked attribute.
  """
  epsIds = [(e,) for e in epsIds]
  curs = conn.cursor()
  curs.executemany('UPDATE episode SET watched = 1 WHERE id = ?', (epsIds))

  unixTime = int(time.time())
  curs.execute('UPDATE show SET date_tracked = ? WHERE id = ?', (unixTime, showId))
  conn.commit()

def resetShow(showId):
  """Update show episodes setting to 0 their watched attribute
  """
  curs = conn.cursor()

  query = 'UPDATE episode SET watched = 0 WHERE show_id = ?'
  curs.execute(query, (showId,) )
  conn.commit()

def deleteShow(showId):
  """Removes a show and all its episodes from the database.
  """
  curs = conn.cursor()

  queryEpisodes = 'DELETE FROM episode WHERE show_id = ?'
  queryShow = 'DELETE FROM show WHERE id = ?'

  curs.execute(queryEpisodes, (showId,) )
  curs.execute(queryShow, (showId,) )
  
  conn.commit()

