# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.lsc.Bind(wx.EVT_LEFT_DCLICK, self.edit)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.cho_phase_id.Bind(wx.EVT_CHOICE, self.on_refresh)
        view.lsc.Bind(wx.EVT_LIST_COL_END_DRAG, self.save_col_sizes)
        view.btn_import.Bind(wx.EVT_BUTTON, self.import_from_file)
        view.btn_members.Bind(wx.EVT_BUTTON, self.load_members)
        view.btn_add.Bind(wx.EVT_BUTTON, self.add)
        view.btn_edit.Bind(wx.EVT_BUTTON, self.edit)
        view.btn_delete.Bind(wx.EVT_BUTTON, self.delete)
        view.btn_create_sort.Bind(wx.EVT_BUTTON, self.create_sort)
        view.btn_delete_sort.Bind(wx.EVT_BUTTON, self.delete_sort)
        view.btn_report_start_list.Bind(wx.EVT_BUTTON, self.report_start_list)

    def go_back(self, event):
        self.presenter.go_back()

    def on_refresh(self, event):
        self.presenter.view_refresh()
        event.Skip()

    def import_from_file(self, event):
        self.presenter.import_from_file()

    def load_members(self, event):
        self.presenter.load_members()

    def add(self, event):
        self.presenter.add()

    def edit(self, event):
        self.presenter.edit()

    def delete(self, event):
        self.presenter.delete()

    def save_col_sizes(self, event):
        self.view.lsc_plus.save_custom_column_width()
    
    def on_select(self, event):
        self.presenter.select_item()
        event.Skip()

    def create_sort(self, event):
        self.presenter.create_sort()

    def delete_sort(self, event):
        self.presenter.delete_sort()

    def report_start_list(self, event):
        self.presenter.report_start_list()