# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.on_close)
        view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_close)
        view.btn_acept.Bind(wx.EVT_BUTTON, self.on_acept)

    def on_close(self, event):
        self.presenter.close()
        event.Skip()

    def on_acept(self, event):
        self.presenter.acept()
        event.Skip()
