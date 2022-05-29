# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.on_cancel)
        view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        view.btn_acept.Bind(wx.EVT_BUTTON, self.on_acept)
        view.txt_name.Bind(wx.EVT_KILL_FOCUS, self.on_category_name)

    def on_cancel(self, event):
        self.presenter.cancel()

    def on_acept(self, event):
        self.presenter.acept()

    def on_category_name(self, event):
        self.view.calculate_category_name()


