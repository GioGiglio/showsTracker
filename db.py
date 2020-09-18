from objects import Show,Episode
import sqlite3
import time

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

# TODO change, remove seasons
def getShows():
  curs = conn.cursor()

  query = '''
  SELECT show.*, s.id, s.number, e.id, e.number, e.name, e.watched
  FROM show JOIN season AS s ON show.id = s.show_id
  JOIN episode AS e ON e.season_id = s.id ORDER BY show.id;
  '''

# show.id, show.name, s.id, s.num, ep.id, ep.num, ep.name, ep.watched
#   |          |        |     |       |      |       |        |
#   0          1        2     3       4      5       6        7

  shows = []
  showIdx = 0
  
  curs.execute(query)
  r1 = curs.fetchone()

  shows.append(Show(r1[1],r1[0]))
  currSeason = Season(r1[3],r1[2])
  currSeason.addEpisode(Episode(r1[6],r1[5],r1[4],r1[7]))

  rows = curs.fetchall()
  for r in rows:
    # if show changed
    if r[0] != shows[showIdx].id:
      shows[showIdx].addSeason(currSeason)
      shows.append(Show(r[1],r[0]))
      showIdx += 1
      
      # update current season
      currSeason = Season(r[3],r[2])
    
    # if season changed
    if r[2] != currSeason.id:
      shows[showIdx].addSeason(currSeason)
      currSeason = Season(r[3],r[2])
    
    # add episode to current season
    currSeason.addEpisode(Episode(r[6],r[5],r[4],r[7]))
  
  # currSeason add current season to last show
  shows[showIdx].addSeason(currSeason)
  return shows

