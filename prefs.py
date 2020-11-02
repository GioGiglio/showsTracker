import json

PREFS_FILE = 'prefs.json'

def _checkPrefsValid(prefs):
  """Checks if the preferences provided are valid.
  If not the function raises a ValueError exception.
  This function is invoked by both load() and write()
  """

  # check if all keys are present
  keys = ('view', 'curr_next_summary', 'eps_list_summary')
  if not all(k in prefs for k in keys):
    raise ValueError('keys missing')

  if prefs['view'] not in ('all','watching'):
    raise ValueError('invalid value for key "view"')

  if prefs['curr_next_summary'] not in ('on','off','only_watched'):
    raise ValueError('invalid value for key "nospoiler"')

  if prefs['eps_list_summary'] not in ('on','off','only_watched'):
    raise ValueError('invalid value for key "nospoiler"')

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
      return prefs

def write(prefs):
  with open(PREFS_FILE,'w') as pfile:
    pfile.write(json.dumps(prefs, indent=4))

