# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.go_back)
        # view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        view.btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        view.btn_delete.Bind(wx.EVT_BUTTON, self.delete)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.btn_move_down.Bind(wx.EVT_BUTTON, self.move_down)
        view.btn_move_up.Bind(wx.EVT_BUTTON, self.move_up)

    def go_back(self, event):
        self.presenter.go_back()

    def on_add(self, event):
        self.presenter.add()

    def delete(self, event):
        self.presenter.delete()

    def move_down(self, event):
        self.presenter.move_down()

    def move_up(self, event):
        self.presenter.move_up()
