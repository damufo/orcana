# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.on_cancel)
        view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        view.btn_acept.Bind(wx.EVT_BUTTON, self.on_acept)

    def on_cancel(self, event):
        self.presenter.cancel()

    def on_acept(self, event):
        self.presenter.acept()
    


