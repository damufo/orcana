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

import os
import re

from .m_fiarna import Model
from .v_fiarna import View
from .i_fiarna import Interactor


def create(parent, config):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(config=config),
            view=View(parent.view),
            interactor=Interactor())


class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.model = model
        self.view = view
        interactor = Interactor()
        interactor.install(self, self.view)
        self.view.view_plus.start(modal=True)

    def set_path(self):
        os.chdir(self.model.referee_tokens.config.app_path_folder)
        print(os.getcwd())

    def about(self):
        self.view.about(self.model.referee_tokens.config)

    def generate(self):
        from_event, to_event, phase, sort_order = self.view.get_values()
        # self.set_path()
        # report_path = self.view.msg.save_file(
        #         suffixes=[".pdf"],
        #         default_file=_("referee_tokens")
        #         )
        config = self.model.referee_tokens.config
        if sort_order == 0:
            file_name = _("referee_tokens_by_lane.pdf")
        else:
            file_name = _("referee_tokens_by_event.pdf")
        file_path = os.path.join(config.work_folder_path, file_name)
        if file_path:
            self.model.referee_tokens.sort_order = sort_order     
            self.model.referee_tokens.report(
                report_path=str(file_path),
                from_event=from_event,
                to_event=to_event,
                phase=phase)
            # self.view.msg.information(_("The operation was successful!"))
            self.view.close()

    def close(self):
        self.view.close()
