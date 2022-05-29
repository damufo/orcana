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

# Copyright (C) 2017 Federacion Galega de Natación (FEGAN) http://www.fegan.org
# Author: Daniel Muñiz Fontoira (2017) <dani@damufo.com>

import time

from specific_classes.database import Database


class Config(object):
    '''
    dbs is database connection
    prefs is a prefs file
    '''

    def __init__(self, app_path_folder, platform):
        '''
        Constructor
        '''
        self.app_name = None
        self.app_version = None
        self.app_description = None
        self.app_copyright = None
        self.app_web_site = None
        self.app_developer = None
        self.app_path_folder = app_path_folder

        self.language = "gl"  # self.prefs.language
#         self.init_localization()
        self.platform = platform
        self.dbs = Database(platform=platform)

    @property
    def current_date(self):
        return str(time.strftime(u"%Y%m%d", time.localtime()))

    @property
    def current_time(self):
        return str(time.strftime(u"%H%M%S", time.localtime(time.time())))

    @property
    def timestamp(self):
        return u"%s%s" % (time.strftime(u"%Y%m%d",
                                        time.localtime()),
                          time.strftime(u"%H%M%S",
                                        time.localtime(time.time())))

    def sleep(self, seconds):
        time.sleep(seconds)

    def close_dbs(self):
        self.dbs.close()
