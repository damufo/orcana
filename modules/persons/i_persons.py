# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.lsc.Bind(wx.EVT_LEFT_DCLICK, self.edit)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.btn_add.Bind(wx.EVT_BUTTON, self.add)
        view.btn_edit.Bind(wx.EVT_BUTTON, self.edit)
        view.btn_delete.Bind(wx.EVT_BUTTON, self.delete)

    def go_back(self, event):
        self.presenter.go_back()
        # if event.CanVeto():
            # event.Veto()
            # return

    def add(self, event):
        self.presenter.add()

    def edit(self, event):
        self.presenter.edit()

    def delete(self, event):
        self.presenter.delete()

