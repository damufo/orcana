import sys
import sys
sys.path.append('/home/damufo/dev/orcana')

from pathlib import Path
import gettext
# from gettext import ngettext
# import locale
import logging

from specific_classes.prefs import Prefs
from specific_classes.config import Config
from specific_classes.champ.champ import Champ
from specific_functions import marks

APP_NAME = 'orcana'
APP_TITLE = 'Orcana'


app_path_folder = '/home/damufo/dev/orcana/'

arg1 = None
if len(sys.argv) > 1:
    arg1 = sys.argv[1]

config_app_dir_path = Path.home().joinpath('.config', APP_NAME)
config_app_dir_path.mkdir(parents=True, exist_ok=True)

prefs = Prefs(
    config_app_dir_path=config_app_dir_path,
    file_name='settings.json')
prefs.load()

prefs["app.language"] = 'gl'

# Localization
if not "app.language" in prefs:
    prefs["app.language"] = 'en'
filename = "locale/messages_{}.mo".format(prefs["app.language"])
try:
    trans = gettext.GNUTranslations(open(filename, "rb"))
except IOError:
    trans = gettext.NullTranslations()
trans.install()

config = Config(prefs=prefs,
    app_name=APP_NAME,
    app_title=APP_TITLE,
    app_path_folder=app_path_folder,
    arg1=arg1)

if sys.platform.lower()[:3] == 'lin':
    config.platform = 'lin'
elif sys.platform.lower()[:3] == 'win':
    config.platform = 'win'

champ = Champ(config=config)
if 'last_path_dbs' in config.prefs and config.prefs['last_path_dbs']:
    champ.load_dbs(dbs_path=config.prefs['last_path_dbs'])

    print(champ.name)
    #xerar series
    champ.auto_gen_heats()

print("Fin")