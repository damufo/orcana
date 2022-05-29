# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.btn_select_candidates.Bind(wx.EVT_BUTTON, self.save_candidates)
        view.btn_new_person.Bind(wx.EVT_BUTTON, self.new_person)
        view.btn_remove_members.Bind(wx.EVT_BUTTON, self.remove_members)
        view.lsc_candidates.Bind(wx.EVT_LIST_COL_END_DRAG, self.save_col_sizes)
        view.lsc_candidates.Bind(wx.EVT_LIST_ITEM_SELECTED, self.select_candidates)
        view.lsc_candidates.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.select_candidates)
        view.btn_move_down.Bind(wx.EVT_BUTTON, self.move_down)
        view.btn_move_up.Bind(wx.EVT_BUTTON, self.move_up)

    def go_back(self, event):
        self.presenter.go_back()
        # if event.CanVeto():
            # event.Veto()
            # return

    def move_down(self, event):
        self.presenter.move_down()

    def move_up(self, event):
        self.presenter.move_up()

    def new_person(self, event):
        self.presenter.new_person()

    def save_candidates(self, event):
        self.presenter.save_candidates()

    def remove_members(self, event):
        self.presenter.remove_members()
    
    def save_col_sizes(self, event):
        self.view.lsc_candidates_plus.save_custom_column_width()
        self.view.lsc_members_plus.reload_custom_column_width()

    def select_candidates(self, event):
        self.presenter.select_candidates()
