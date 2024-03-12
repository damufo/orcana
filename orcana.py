# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2020 Daniel Muñiz Fontoira
# Author: Daniel Muñiz Fontoira (2020) <dani@damufo.com>

import sys
from pathlib import Path
import codecs
import json
import requests

import wx
import locale
import gettext
from classes.wxp.view_plus import ViewPlus
from classes.wxp.list_ctrl_plus import ListCtrlPlus
from classes.wxp.spl_plus import SplPlus
from specific_classes.app_icon import app_icon
from specific_classes.prefs import Prefs
from specific_classes.config import Config
from specific_classes.champ.champ import Champ
from modules.main.p_main import Presenter


try:
    # Get app current version
    remote_url = 'https://gitlab.com/damufo/orcana/-/raw/master/VERSION.txt?ref_type=heads'
    data = requests.get(remote_url)
    APP_CURRENT_VERSION = data.text
except:
    APP_CURRENT_VERSION = ''

APP_NAME = 'orcana'
APP_TITLE = 'Orcana'
APP_VERSION = "0.0.11beta"
DBS_VERSION = 5
APP_VERSION_DATE = "2024-03-12"

if getattr(sys, 'frozen', False): # Running as compiled
    running_dir = sys._MEIPASS + "/_internal/" # pylint: disable=no-member
    APP_PATH_FOLDER = Path(sys._MEIPASS)
else:
    APP_PATH_FOLDER = Path(__file__).parent.absolute()


class Application(wx.App):

    def OnInit(self):
        print(APP_PATH_FOLDER)
        # self.translate(app_path_folder)
        self.name = "{}-{}".format(APP_NAME, wx.GetUserId())

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
        self.localization(prefs=prefs)
        #self.translate(app_path_folder=app_path_folder)

        config = Config(prefs=prefs,
            app_name=APP_NAME,
            app_title=APP_TITLE,
            app_version=APP_VERSION,
            app_current_version=APP_CURRENT_VERSION,
            app_version_date=APP_VERSION_DATE,
            app_path_folder=APP_PATH_FOLDER,
            arg1=arg1)
        
        if sys.platform.lower()[:3] == 'lin':
            config.platform = 'lin'
        elif sys.platform.lower()[:3] == 'win':
            config.platform = 'win'

        ViewPlus.prefs = config.prefs
        ViewPlus.app_icon = app_icon.GetIcon()
        ViewPlus.image_path = APP_PATH_FOLDER / "images" / "buttons" / "24"

        ListCtrlPlus.prefs = config.prefs
        SplPlus.prefs = config.prefs

        champ = Champ(config=config)
        Presenter(champ=champ)
        return True

    def localization(self, prefs):
        '''prepare l10n'''
        if not "app.language" in prefs:
            prefs["app.language"] = 'en'
        filename = str(APP_PATH_FOLDER) + "/locale/{}/LC_MESSAGES/orcana.mo".format(prefs["app.language"])
        try:
            trans = gettext.GNUTranslations(open(filename, "rb"))
        except IOError:
            trans = gettext.NullTranslations()
        trans.install()

    # def translate(self, app_path_folder):
    #     has_translations = False
    #     app_path_folder_locale = app_path_folder / 'locale'
    #     app_path_folder_locale2 = app_path_folder / 'locale' / 'gl' / 'LC_MESSAGES'
    #     localedirs = (str(app_path_folder_locale), '~/.local/share/locale', app_path_folder_locale2)
    #     for i in localedirs:
    #         if gettext.find('orcana', localedir=i, languages=['gl']):
    #             has_translations = True
    #             gettext.install(domain='orcana', localedir=i)
    #             break
    #     if not has_translations:
    #         trans = gettext.NullTranslations()
    #         trans.install()

try:
    app = Application()
    app.MainLoop()
except SystemExit:
    sys.exit(0)
