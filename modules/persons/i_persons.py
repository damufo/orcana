# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.lsc_persons.Bind(wx.EVT_LEFT_DCLICK, self.edit)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.btn_add.Bind(wx.EVT_BUTTON, self.add)
        view.btn_edit.Bind(wx.EVT_BUTTON, self.edit)
        view.btn_delete.Bind(wx.EVT_BUTTON, self.delete)
        view.lsc_persons.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_person)
        view.lsc_persons.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_select_person)
        view.lsc_persons.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_select_person)
        view.btn_add_insc.Bind(wx.EVT_BUTTON, self.add_insc)
        view.btn_edit_insc.Bind(wx.EVT_BUTTON, self.edit_insc)
        view.btn_delete_insc.Bind(wx.EVT_BUTTON, self.delete_insc)
        view.spl_persons.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.on_splitter)     

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

    def add_insc(self, event):
        self.presenter.add_insc()

    def edit_insc(self, event):
        self.presenter.edit_insc()

    def delete_insc(self, event):
        self.presenter.delete_insc()
    
    def on_select_person(self, event):
        self.presenter.select_person()
    
    def on_splitter(self, event):
        print("splitter: ", self.view.spl_persons.GetSashPosition())

