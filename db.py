from objects import Show,Season,Episode
import sqlite3

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

def saveShow(show):
  curs = conn.cursor()
  
  # insert show
  curs.execute('INSERT INTO show VALUES(?,?)', (show.id, show.name) )
  conn.commit()

  # insert seasons and episodes
  for season in show.seasons:
    curs.execute('INSERT INTO season VALUES(?,?,?)', (season.id, show.id, season.number) )
    episodes = [(e.id, season.id, e.number, e.name, 0) for e in season.episodes]
    curs.executemany('INSERT INTO episode VALUES(?,?,?,?,?)', episodes)
    conn.commit()

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

def getShowsAndSeasons():
  curs = conn.cursor()
  query = 'SELECT show.*, season.* FROM show JOIN season ON show.id = season.show_id ORDER BY show.id;'
  curs.execute(query)
  
  shows = []
  curr= 0
  rows = curs.fetchall()
  for r in rows:
    if not shows:
      shows.append(Show(r[1],r[0]))
    
    # check if r has a different show
    if r[0] != shows[curr].id:
      curr += 1
      shows.append(Show(r[1],r[0]))
    
    shows[curr].addSeason(Season(r[4],r[2]))
  return shows
