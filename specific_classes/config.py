# -*- coding: utf-8 -*-

          
# import codecs
# from pathlib import Path
# import json
# from .prefs import Prefs
from classes.sqlite_plus import SqlitePlus
from specific_classes.core.genders import Genders
from specific_classes.core.issues import Issues
from specific_classes.core.choices import Choices


class Config(object):

    def __init__(self, prefs, app_name, app_title, app_path_folder, arg1):
        self.prefs = prefs
        self.app_name = app_name
        self.app_title = app_title
        self.app_version = "0.0.1"
        self.app_version_date = "2021-08-24"
        self.app_description = _("A simple championships manager.")
        self.app_copyright = "(C) 2020 Daniel Muñiz Fontoira"
        self.app_web_site = "https://gitlab.com/damufo/{}".format(app_name)
        self.app_developer = "Daniel Muñiz Fontoira"
        self.app_license = _(
"Copyright (C) 2020  Daniel Muñiz Fontoira\n\n"
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

        self.app_path_folder = app_path_folder
        self.arg1 = arg1

        self.dbs = SqlitePlus()

        self.pool_length = Choices(choices=(
            (25, '25'),
            (50, '50'),
            (450, '450'),
            ))
        self.pool_lanes = Choices(choices=(
            (5, '5'),
            (6, '6'),
            (8, '8'),
            (10, '10'),
            ))            
        self.chrono_type = Choices(choices=(
            ('M', _('Manual')),
            ('E', _('Electronic')),
            ))
        self.estament = Choices(choices=(
            ('DEPOR', _('Deportista')),
            ('MASTE', _('Master')),
            ))
        self.gender = Choices(choices=(
            ('F', _('Female')),
            ('M', _('Male')),
            ))
        # self.category_type = Choices(choices=(
        #     ('A', _('Absolute')),
        #     ('C', _('Category')),
        #     ))

        self.issues = Issues(self)
        self.issues.load_items_from_dbs()
        self.genders = Genders(self)
        self.genders.load_items_from_dbs()
        self.views = {}

    def get_gender_name(self, gender_id):
        if gender_id == 'M':
            gender_name = _('Male')
        elif gender_id == 'F':
            gender_name = _('Female')
        elif gender_id == 'X':
            gender_name = _('Mixed')
        else:
            gender_name = ''
        return gender_name

        # self.issues_id = Choices(choices=(
        #     ('BAI', _('Baixa')),
        #     ('RET', _('Retirado')),
        #     ('NPR', _('Non presentado/a')),
        #     ('DNI', _('Nado irregular')),
        #     ('DVI', _('Viraxe irregular')),
        #     ('DSA', _('Saída anticipada')),
        #     ))