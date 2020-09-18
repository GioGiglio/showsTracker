from objects import *
import re

def promptSelectShow(showsData):
  # regex to match html tags
  htmlTagsRe = re.compile('<.*?>')
  
  i = 0
  for s in showsData[:5]:

    s = s['show']

    # remove html tags from summary
    summaryText = re.sub(htmlTagsRe, '', s['summary'][:200]) if s['summary'] else ''

    print('#{}\nName: {}\nGenres: {}\nSummary: {}...\n'.format(
          i,
          s['name'],
          ", ".join(s['genres']),
          summaryText
    ))
    i += 1

  while True:
    try:
      selected = int(input('Select the show: #'))
      if selected < 0 or selected >= i:
        raise ValueError()
      break
    except ValueError:
      print('Invalid selection!')

  id = showsData[selected]['show']['id']
  name = showsData[selected]['show']['name']
  return Show(id, name)

