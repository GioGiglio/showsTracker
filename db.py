import sqlite3

DB_PATH = 'showsTracker.db'
conn = None

def __connect():
  return sqlite3.connect(DB_PATH)

def init():
  global conn
  conn = __connect()

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
  query = '''SELECT show.id, show.name, s.id as s_id, s.number as s_num,
  e.id as e_id, e.number as e_num, e.name as e_name, e.watched as e_wtch
  FROM show JOIN season s ON show.id=s.show_id JOIN episode e on s.id = e.season_id;'''
