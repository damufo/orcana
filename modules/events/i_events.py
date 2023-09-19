# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.btn_move_down.Bind(wx.EVT_BUTTON, self.move_down)
        view.btn_move_up.Bind(wx.EVT_BUTTON, self.move_up)
        view.lsc.Bind(wx.EVT_LEFT_DCLICK, self.edit)
        view.btn_add.Bind(wx.EVT_BUTTON, self.add)
        view.btn_edit.Bind(wx.EVT_BUTTON, self.edit)
        view.btn_delete.Bind(wx.EVT_BUTTON, self.delete)

    def go_back(self, event):
        self.presenter.go_back()

    def move_down(self, event):
        self.presenter.move_down()

    def move_up(self, event):
        self.presenter.move_up()

    def add(self, event):
        self.presenter.add()

    def edit(self, event):
        self.presenter.edit()

    def delete(self, event):
        self.presenter.delete()
