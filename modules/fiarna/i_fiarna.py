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

import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.btn_close.Bind(wx.EVT_BUTTON, self.on_close)
        view.btn_gen_referee_tokens.Bind(wx.EVT_BUTTON, self.on_generate)
        # view.btn_about.Bind(wx.EVT_BUTTON, self.on_about)

    def on_generate(self, event):
        self.presenter.generate()
        event.Skip()

    def on_about(self, event):
        self.presenter.about()
        event.Skip()

    def on_close(self, event):
        self.presenter.close()
        event.Skip()
