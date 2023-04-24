# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.on_cancel)
        view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        view.btn_add_category.Bind(wx.EVT_BUTTON, self.on_add_category)
        view.btn_acept.Bind(wx.EVT_BUTTON, self.on_acept)
        view.lsc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.select_categories)
        view.lsc.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.select_categories)

    def on_cancel(self, event):
        self.presenter.cancel()

    def on_add_category(self, event):
        self.presenter.add_category()

    def on_acept(self, event):
        self.presenter.acept()

    def select_categories(self, event):
        self.presenter.select_categories()