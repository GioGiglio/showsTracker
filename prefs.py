import json
from collections import namedtuple

PREFS_FILE = 'prefs.json'

View = namedtuple('View', 'all watching')
OverviewSummary = namedtuple('OverviewSummary', 'on off onlyWatched')
EpsListSummary = namedtuple('EpsListSummary', 'on off onlyWatched')

class Prefs:
  def __init__(self, prefs):
    value = prefs['view']
    self.view = View(value=='all', value=='watching')
    value = prefs['shows_overview_summary']
    self.overviewSummary = OverviewSummary(value=='on', value=='off', value=='only_watched')
    value = prefs['episodes_list_summary']
    self.epsListSummary = EpsListSummary(value=='on', value=='off', value=='only_watched')

def _checkPrefsValid(prefs):
  """Checks if the preferences provided are valid.
  If not the function raises a ValueError exception.
  This function is invoked by both load() and write()
  """

  # check if all keys are present
  keys = ('view', 'shows_overview_summary', 'episodes_list_summary')
  if not all(k in prefs for k in keys):
    raise ValueError('keys missing')

  if prefs['view'] not in ('all','watching'):
    raise ValueError('invalid value for key "view"')

  if prefs['shows_overview_summary'] not in ('on','off','only_watched'):
    raise ValueError('invalid value for key "shows_overview_summary"')

  if prefs['episodes_list_summary'] not in ('on','off','only_watched'):
    raise ValueError('invalid value for key "episodes_list_summary"')

def load():
  with open(PREFS_FILE,'r') as pfile:
    try:
      prefs = json.load(pfile)
      _checkPrefsValid(prefs)
    except json.decoder.JSONDecodeError:
      print('-- error: prefs: invalid json file!')
      exit(1)
    except ValueError as e:
      print('-- error: prefs:', str(e))
      exit(1)
    else:
      return Prefs(prefs)

def write(prefs):
  with open(PREFS_FILE,'w') as pfile:
    pfile.write(json.dumps(prefs, indent=4))

