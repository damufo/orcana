# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.lsc.Bind(wx.EVT_LEFT_DCLICK, self.edit)
        view.lsc.Bind(wx.EVT_LIST_COL_END_DRAG, self.save_col_sizes)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.cho_phase_id.Bind(wx.EVT_CHOICE, self.on_phase_change)
        view.cho_phase_category_id.Bind(wx.EVT_CHOICE, self.on_phase_category_change)
        view.btn_edit.Bind(wx.EVT_BUTTON, self.edit)

    def go_back(self, event):
        self.presenter.go_back()

    def on_phase_change(self, event):
        self.presenter.phase_change()
        event.Skip()

    def on_phase_category_change(self, event):
        self.presenter.phase_category_change()
        event.Skip()

    def edit(self, event):
        self.presenter.edit()

    def save_col_sizes(self, event):
        self.view.lsc_plus.save_custom_column_width()
