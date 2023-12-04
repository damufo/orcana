# -*- coding: utf-8 -*-

          
# import codecs
# from pathlib import Path
# import json
# from .prefs import Prefs
from classes.sqlite_plus import SqlitePlus
from specific_classes.core.genders import Genders
from specific_classes.core.styles import Styles
from specific_classes.core.issues import Issues
from specific_classes.core.progressions import Progressions
from specific_classes.core.choices import Choices
from specific_functions import files

class Config(object):

    def __init__(
        self, prefs, app_name, app_title, app_version, 
        app_version_date, app_path_folder, arg1):
        self.prefs = prefs
        self.app_name = app_name
        self.app_title = app_title
        self.app_version = app_version
        self.app_version_date = app_version_date
        self.app_description = _("A pool swimming championship management application.")
        self.app_copyright = "(C) 2023 Daniel Muñiz Fontoira"
        self.app_web_site = "https://gitlab.com/damufo/{}".format(app_name)
        self.app_developer = "Daniel Muñiz Fontoira"
        self.app_license = _(
"{}\n\n"
"This program is free software: you can redistribute it and/or modify "
"it under the terms of the GNU General Public License as published by "
"the Free Software Foundation, either version 3 of the License, or "
"(at your option) any later version.\n\n"
"This program is distributed in the hope that it will be useful, "
"but WITHOUT ANY WARRANTY; without even the implied warranty of "
"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
"GNU General Public License for more details.\n\n"
"You should have received a copy of the GNU General Public License "
"along with this program.  If not, see <http://www.gnu.org/licenses/>.")
        self.app_license = self.app_license.format(self.app_copyright)

        self.app_path_folder = app_path_folder
        self.arg1 = arg1

        self.dbs = SqlitePlus()

        self.pool_length = Choices(choices=(
            (25, '25'),
            (50, '50'),
            ))           
        self.chrono_type = Choices(choices=(
            ('M', _('Manual')),
            ('E', _('Electronic')),
            ))
        self.estament = Choices(choices=(
            ('DEPOR', 'Deportista'),
            ('MASTE', 'Master'),
            ))
        # self.gender = Choices(choices=(
        #     ('F', _('Female')),
        #     ('M', _('Male')),
        #     ('X', _('Mixed')),
        #     ))
        self.event_code = Choices(choices=(
            ('25L', _('25 m Free')),
            ('50L', _('50 m Free')),
            ('100L', _('100 m Free')),
            ('200L', _('200 m Free')),
            ('400L', _('400 m Free')),
            ('800L', _('800 m Free')),
            ('1500L', _('1500 m Free')),
            ('50M', _('50 m Butterfly')),
            ('100M', _('100 m Butterfly')),
            ('200M', _('200 m Butterfly')),
            ('50E', _('50 m Backstroke')),
            ('100E', _('100 m Backstroke')),
            ('200E', _('200 m Backstroke')),
            ('50B', _('50 m Breaststroke')),
            ('100B', _('100 m Breaststroke')),
            ('200B', _('200 m Breaststroke')),
            ('100S', _('100 m Medley')),
            ('200S', _('200 m Medley')),
            ('400S', _('400 m Medley')),
            ('4X25L', _('4x25 m Free')),
            ('4X50L', _('4x50 m Free')),
            ('4X100L', _('4x100 m Free')),
            ('4X200L', _('4x200 m Free')),
            ('4X25S', _('4x25 m Medley')),
            ('4X50S', _('4x50 m Medley')),
            ('4X100S', _('4x100 m Medley')),
            ))
        # self.category_type = Choices(choices=(
        #     ('A', _('Absolute')),
        #     ('C', _('Category')),
        #     ))

        self.issues = Issues(self)
        self.issues.load_items_from_dbs()
        self.genders = Genders(self)
        self.genders.load_items_from_dbs()
        self.styles = Styles(self)
        self.styles.load_items_from_dbs()
        self.progressions = Progressions(self)
        self.progressions.load_items_from_dbs()
        self.views = {}

    @property
    def work_folder_path(self):
        work_folder_path = '' 
        if self.prefs['last_path_dbs']:
            work_folder_path = files.get_folder_path(file_path=self.prefs['last_path_dbs'])
        return work_folder_path