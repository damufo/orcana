# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.btn_close.Bind(wx.EVT_BUTTON, self.go_back)
        view.cho_event_id.Bind(wx.EVT_CHOICE, self.on_refresh)

    def go_back(self, event):
        self.presenter.go_back()
        # if event.CanVeto():
            # event.Veto()
            # return

    def on_refresh(self, event):
        self.presenter.view_refresh()
        event.Skip()

