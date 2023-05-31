# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.lsc.Bind(wx.EVT_LEFT_DCLICK, self.edit)
        view.btn_categories.Bind(wx.EVT_BUTTON, self.categories)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.btn_move_down.Bind(wx.EVT_BUTTON, self.move_down)
        view.btn_move_up.Bind(wx.EVT_BUTTON, self.move_up)
        view.btn_copy_cat.Bind(wx.EVT_BUTTON, self.copy_phase_categories)
        view.btn_paste_cat.Bind(wx.EVT_BUTTON, self.paste_phase_categories)
        view.btn_sort.Bind(wx.EVT_BUTTON, self.sort)
        view.btn_start_list.Bind(wx.EVT_BUTTON, self.start_list)
        view.btn_add.Bind(wx.EVT_BUTTON, self.add)
        view.btn_edit.Bind(wx.EVT_BUTTON, self.edit)
        view.btn_delete.Bind(wx.EVT_BUTTON, self.delete)

    def categories(self, event):
        self.presenter.phase_categories()

    def go_back(self, event):
        self.presenter.go_back()

    def move_down(self, event):
        self.presenter.move_down()

    def move_up(self, event):
        self.presenter.move_up()

    def copy_phase_categories(self, event):
        self.presenter.copy_phase_categories()

    def paste_phase_categories(self, event):
        self.presenter.paste_phase_categories()

    def sort(self, event):
        self.presenter.sort()

    def start_list(self, event):
        self.presenter.start_list()

    def add(self, event):
        self.presenter.add()

    def edit(self, event):
        self.presenter.edit()

    def delete(self, event):
        self.presenter.delete()