# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.on_cancel)
        view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        view.btn_add_person.Bind(wx.EVT_BUTTON, self.on_add_person)
        view.txt_person_full_name.Bind(wx.EVT_KILL_FOCUS, self.on_person_full_name)
        view.txt_person_full_name.Bind(wx.EVT_CHAR, self.on_person_full_name_change)
        view.btn_acept.Bind(wx.EVT_BUTTON, self.on_acept)
        view.chb_classify.Bind(wx.EVT_CHECKBOX, self.on_classify)

    def on_cancel(self, event):
        self.presenter.cancel()

    def on_add_person(self, event):
        self.presenter.add_person()

    def on_acept(self, event):
        self.presenter.acept()
    
    def on_person_full_name(self, event):
        self.presenter.person_full_name()

    def on_classify(self, event):
        self.view.set_classify()

    def on_person_full_name_change(self, event):
        skip_keys = (wx.WXK_TAB, wx.WXK_SHIFT, wx.WXK_RETURN)
        kc = event.GetKeyCode()
        if kc not in skip_keys:
            print('change on')
            self.presenter.model.person_full_name_change = True
        event.Skip()

