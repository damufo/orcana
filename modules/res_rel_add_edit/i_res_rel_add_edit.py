# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.on_cancel)
        view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        view.btn_add_entity.Bind(wx.EVT_BUTTON, self.on_add_entity)
        view.txt_entity_name.Bind(wx.EVT_KILL_FOCUS, self.on_entity_name)
        view.txt_entity_name.Bind(wx.EVT_CHAR, self.on_entity_name_change)
        view.btn_acept.Bind(wx.EVT_BUTTON, self.on_acept)
        view.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)

    def on_cancel(self, event):
        self.presenter.cancel()

    def on_add_entity(self, event):
        self.presenter.add_entity()

    def on_acept(self, event):
        self.presenter.acept()

    def on_delete(self, event):
        self.presenter.delete()
    
    def on_entity_name(self, event):
        self.presenter.entity_name()

    def on_entity_name_change(self, event):
        skip_keys = (wx.WXK_TAB, wx.WXK_SHIFT, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER)
        kc = event.GetKeyCode()
        if kc not in skip_keys:
            print('change on')
            self.presenter.model.entity_name_change = True
        event.Skip()
        


