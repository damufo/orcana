# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.Bind(wx.EVT_CLOSE, self.on_close)
        view.btn_cancel.Bind(wx.EVT_BUTTON, self.on_close)
        
        view.spn_width_px.Bind(wx.EVT_SPINCTRL, self.on_width_change)
        view.spn_width_px.Bind(wx.EVT_KILL_FOCUS, self.on_width_change)
        view.spn_width_px.Bind(wx.EVT_KEY_UP, self.on_width_change)
        
        view.spn_height_px.Bind(wx.EVT_SPINCTRL, self.on_height_change)
        view.spn_height_px.Bind(wx.EVT_KILL_FOCUS, self.on_height_change)
        view.spn_height_px.Bind(wx.EVT_KEY_UP, self.on_height_change)

        view.spn_width_percent.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_width_change)
        view.spn_width_percent.Bind(wx.EVT_KILL_FOCUS, self.on_width_change)
        view.spn_width_percent.Bind(wx.EVT_KEY_UP, self.on_width_change)
        
        view.spn_height_percent.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_height_change)
        view.spn_height_percent.Bind(wx.EVT_KILL_FOCUS, self.on_height_change)
        view.spn_height_percent.Bind(wx.EVT_KEY_UP, self.on_height_change)
        
        view.cho_units.Bind(wx.EVT_CHOICE, self.on_change_units)
        
        view.btn_acept.Bind(wx.EVT_BUTTON, self.on_acept)

    def on_close(self, event):
        self.presenter.close()
        event.Skip()

    def on_acept(self, event):
        self.presenter.acept()
        event.Skip()

    def on_width_change(self, event):
        self.view.update_height()
        event.Skip()

    def on_height_change(self, event):
        self.view.update_width()
        event.Skip()

    def on_change_units(self, event):
        self.view.change_units()
        event.Skip()
