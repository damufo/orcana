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
from wx import adv
from wx.lib.wordwrap import wordwrap

from modules.fiarna.w_fiarna import Fiarna
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
# from classes.wxp.win_control import WinControl


class View(Fiarna):
    """
    wxformbuilder: replace: AddSpacer() -> AddStretchSpacer()
    """

    def __init__(self, parent):
        Fiarna.__init__(self, parent)
        self.SetName('fiarna')
        self.view_plus = ViewPlus(self)
        # self.win_control = WinControl()
        self.msg = Messages(self)
        self.launcher = None
        self.closed = False

    def get_values(self):
        from_event = self.spn_from_event.GetValue()
        to_event = self.spn_to_event.GetValue()
        phase = self.cho_phase.GetSelection()
        sort_order = self.cho_sort.GetSelection()
        return from_event, to_event, phase, sort_order

    def about(self, config):
        info = adv.AboutDialogInfo()
        info.SetName(config.app_name)
        info.SetVersion(config.app_version)
        info.SetDescription(
            wordwrap(
                config.app_description,
                500,
                dc=wx.ClientDC(self.panel), breakLongWords=False))
        info.SetCopyright(config.app_copyright)
        info.SetWebSite(config.app_web_site, _("Fiarna website"))
        info.AddDeveloper(config.app_developer)
        info.AddTranslator(config.app_developer)
        info.License = wordwrap(config.app_license, 500,
                                wx.ClientDC(self.panel))

        info.SetIcon(self.view_plus.app_icon)
        adv.AboutBox(info=info, parent=self)

    def close(self):
        for child in self.GetChildren():
            if isinstance(child, wx.Frame):
                print(child.GetLabel())
                # BUGFIX: child label
                print("Repair this child.GetLabel\n"
                      "ver que isto tamén funciona en windows")
                child.msg.warning(_(u"First close window %s.") % child.Title)
                break
        else:
            self.closed = True
            self.Close()
            self.Destroy()
